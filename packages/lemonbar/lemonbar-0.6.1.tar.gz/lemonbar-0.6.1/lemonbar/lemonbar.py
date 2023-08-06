import asyncio
import datetime
import logging
import select
from subprocess import PIPE, Popen
from typing import List, Optional, Dict

from .async_utils import state_kept_await
from .models.bar_geometry import BarGeometry
from .models.bar_placement import BarPlacement
from .models.lemonbar_arguments import LemonbarArguments
from .models.monitor import MonitorId
from .module import Module

_DEFAULT_LOGGER = logging.getLogger("lemonbar")


class Lemonbar:
    def __init__(
            self,
            modules: List[Module],
            geometry: BarGeometry = None,
            outputs: Optional[List[MonitorId]] = None,
            placement: BarPlacement = BarPlacement.TOP,
            force_dock: bool = False,
            fonts: Optional[List[str]] = None,
            permanent: bool = False,
            title: Optional[str] = "",
            underline_width: int = 1,
            background_color: Optional[str] = None,
            foreground_color: Optional[str] = None,
            underline_color: Optional[str] = None,
            logger: logging.Logger = _DEFAULT_LOGGER
    ):
        self._logger = logger
        self._lemonbar_args = LemonbarArguments.build(
            geometry=geometry,
            screen_outputs=outputs or [],
            placement=placement,
            force_dock=force_dock,
            fonts=fonts or [],
            permanent=permanent,
            wm_name=title,
            underline_width=underline_width,
            underline_color=underline_color,
            background_color=background_color,
            foreground_color=foreground_color
        )

        self._command = self._lemonbar_args.get_command()
        self._unsafe_lemonbar_process: Optional[Popen] = None

        self._modules = modules
        self._module_last_render: Dict[Module, datetime.datetime] = {}
        self._render_cache: Dict[Module, str] = {}

    async def attach(self):
        try:
            self._logger.info("Attaching to Lemonbar process stdout")
            while True:
                start_time = datetime.datetime.now()
                self._logger.debug("Starting module render cycle", extra={
                    'start_time': start_time
                })
                await self._module_cycle()
                end_time = datetime.datetime.now()
                interval = end_time - start_time
                self._logger.debug(f"Finished module render cycle in {interval}", extra={
                    'start_time': start_time,
                    'end_time': end_time,
                    'interval': interval
                })
        finally:
            self.close()

    async def _module_cycle(self):
        event_pipe = self._lemonbar_process.stdout

        readables, writables, exceptions = select.select(
            [event_pipe], [], [event_pipe],
            self.minimum_wait_time.total_seconds()
        )

        if event_pipe in exceptions:
            raise RuntimeError("An error occurred waiting for Lemonbar to write!")

        event = event_pipe.readline().rstrip() if event_pipe in readables else None

        render_cycles = [state_kept_await(module, self._handle_module_cycle(module, event)) for module in self._modules]
        for cycle_data in asyncio.as_completed(render_cycles):
            module, render_value = await cycle_data
            had_exception = isinstance(render_value, Exception)
            try:
                if had_exception:
                    raise render_value

                if not isinstance(render_value, (str, bytes)):
                    raise TypeError("Render method must return a string or bytes!")

                self._lemonbar_process.stdin.write(render_value)
            except Exception as e:
                self._logger.exception("Failed to render module!", extra={
                    'module': repr(module)
                })
                render_value = f"ERROR: {e}"
                self._lemonbar_process.stdin.write(render_value)
                had_exception = True
            finally:
                if not had_exception or module.config.cache_exceptions:
                    self._render_cache[module] = render_value
                    self._module_last_render[module] = datetime.datetime.now()

        self._lemonbar_process.stdin.write('\n')
        self._lemonbar_process.stdin.flush()

    async def _handle_module_cycle(self, module: Module, event: Optional[str]) -> str:
        should_handle_event = False
        if event and await module.should_handle_event(event):
            await module.handle_event(event)
            should_handle_event = True

        current_time = datetime.datetime.now()
        module_config = module.config

        last_render_time = self._module_last_render.get(module)
        next_render_time = last_render_time + module_config.minimum_render_interval if last_render_time else None
        passed_render_interval = not next_render_time or current_time >= next_render_time
        force_render_on_event = should_handle_event and module_config.force_render_on_event

        should_render = (passed_render_interval or force_render_on_event) and await module.should_render()
        render_value = self._render_cache.get(module)
        if should_render:
            render_value = await module.render()

        return render_value

    @property
    def minimum_wait_time(self) -> datetime.timedelta:
        return min([module.config.minimum_render_interval for module in self._modules])

    def open(self):
        self._unsafe_lemonbar_process = Popen(
            self._command,
            stdin=PIPE,
            stdout=PIPE,
            encoding='UTF-8'
        )

    def close(self):
        self._logger.info("Closing connection to Lemonbar gracefully.")
        self._lemonbar_process.kill()

    @property
    def _lemonbar_process(self) -> Popen:
        if self._unsafe_lemonbar_process is None:
            raise ValueError("You must initialize the connection to lemonbar by calling `open()` or using `with`")

        return self._unsafe_lemonbar_process

    def __enter__(self):
        self.open()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

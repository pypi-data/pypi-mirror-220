import datetime
from time import strftime
from typing import Optional

from lemonbar import formatters
from lemonbar.module import Module

_EVENT_NAME = "toggle_clock"


class Clock(Module):
    _CONFIG = Module.Config(
        minimum_render_interval=datetime.timedelta(milliseconds=700),
        force_render_on_event=True,
        cache_exceptions=True
    )

    def __init__(self):
        """A simple clock.

        The clock can be clicked and will switch to the date for a period of
        time.
        """
        super().__init__()
        self._toggled_at: Optional[datetime.datetime] = None

    async def render(self):
        # If the clock has been toggled for more than a certain period of time
        if self._toggled_at and datetime.datetime.now() > self._toggled_at + datetime.timedelta(seconds=5):
            self._toggled_at = None  # Automatically toggle back to the clock

        if self._toggled_at:
            return formatters.button(
                formatters.Button.LEFT,
                _EVENT_NAME,
                strftime('%d/%m/%Y')
            )
        else:
            return formatters.button(
                formatters.Button.LEFT,
                _EVENT_NAME,
                strftime('%H:%M:%S')
            )

    async def should_render(self) -> bool:
        return True

    async def handle_event(self, event):
        if not self._toggled_at:
            self._toggled_at = datetime.datetime.now()
        else:
            self._toggled_at = None

    async def should_handle_event(self, event: str) -> bool:
        return event.strip() == _EVENT_NAME

    @property
    def config(self) -> Module.Config:
        return self._CONFIG

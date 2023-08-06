import datetime
from time import strftime
from typing import Optional

from lemonbar import CommandHandler, Button
from lemonbar.module import Module

_EVENT_NAME = "toggle_clock"


class Clock(Module, CommandHandler):
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
        self.register_command(_EVENT_NAME, Button.LEFT, lambda button: Clock.toggle(self, button))

    async def render(self):
        # If the clock has been toggled for more than a certain period of time
        if self._toggled_at and datetime.datetime.now() > self._toggled_at + datetime.timedelta(seconds=5):
            self._toggled_at = None  # Automatically toggle back to the clock

        if self._toggled_at:
            return self.as_command(
                _EVENT_NAME,
                strftime('%d/%m/%Y')
            )
        else:
            return self.as_command(
                _EVENT_NAME,
                strftime('%H:%M:%S')
            )

    async def should_render(self) -> bool:
        return True

    def toggle(self, button: Button):
        if not self._toggled_at:
            self._toggled_at = datetime.datetime.now()
        else:
            self._toggled_at = None

    @property
    def config(self) -> Module.Config:
        return self._CONFIG

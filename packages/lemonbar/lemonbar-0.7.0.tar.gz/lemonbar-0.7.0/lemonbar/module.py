import abc
import dataclasses
import datetime


class Module(abc.ABC):

    @abc.abstractmethod
    async def render(self) -> str:
        """
        :return: The value to render to the Lemonbar
        """

    @abc.abstractmethod
    async def should_render(self) -> bool:
        """
        :return: True if the `render` method should be called next render cycle
        """

    @property
    def config(self) -> 'Module.Config':
        """
        :return: Module configuration
        """
        return Module.Config()

    @dataclasses.dataclass
    class Config:
        """
        :param minimum_render_interval: The minimum amount of time to wait between renders in seconds.
            During the wait, a cached value of the render will be used instead.
            A render call is guaranteed to occur **at least** after <minimum update time>
        :param force_render_on_event: If an event is received and it passes `should_handle_event`
            and `should_render`, ignore the `minimum_render_time` and call `render`.
        :param cache_exceptions: If true, if an exception is thrown during render
            it is cached and render is only called again if <minimum_render_interval> has passed
        """
        minimum_render_interval: datetime.timedelta = datetime.timedelta(seconds=1)
        force_render_on_event: bool = True
        cache_exceptions: bool = True


class EventHandler(abc.ABC):
    @abc.abstractmethod
    async def handle_event(self, event: str):
        """
        Called when <event> is received through stdout communication with Lemonbar
        if `should_handle_event` returns True.
        """

    @abc.abstractmethod
    async def should_handle_event(self, event: str) -> bool:
        """
        Called when <event> is received through stdout communication with Lemonbar

        :param event: The stdout *line* from Lemonbar
        :return: True if the `handle_event` should be called.
        """

import dataclasses
from typing import Dict, Callable, Any, List

import lemonbar.formatters as formatters
from lemonbar.module import EventHandler


class CommandHandler(EventHandler):
    """
    Wrapper around event handling to make creating commands (buttons)
    much simpler.
    """

    def __init__(self):
        self.__commands: Dict[str, List[CommandHandler._Command]] = {}

    async def handle_event(self, event: str):
        commands = self.__commands.get(event)
        for command in commands:
            command.handler(command.button)

    async def should_handle_event(self, event: str) -> bool:
        return event in self.__commands

    def register_command(self, name: str, button: formatters.Button, handler: Callable[[formatters.Button], Any]):
        command_handlers = self.__commands.get(name, [])
        command_handlers.append(CommandHandler._Command(handler, button))
        self.__commands[name] = command_handlers

    def as_command(self, name: str, message: str) -> str:
        commands = self.__commands.get(name)
        if not commands:
            raise ValueError(f"Command {name} is not registered!")

        for command in commands:
            message = formatters.button(
                command.button,
                name,
                message
            )

        return message

    @dataclasses.dataclass
    class _Command:
        handler: Callable[[formatters.Button], Any]
        button: formatters.Button

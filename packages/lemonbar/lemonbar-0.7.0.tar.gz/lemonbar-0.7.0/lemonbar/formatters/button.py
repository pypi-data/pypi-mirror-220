from enum import IntEnum

from lemonbar.formatters._formatter import lemon_formatting


class Button(IntEnum):
    LEFT = 1
    MIDDLE = 2
    RIGHT = 3
    SCROLL_UP = 4
    SCROLL_DOWN = 5


def button(trigger_button: Button, command_name: str, message: str) -> str:
    tag = f'A{trigger_button.value}'
    return lemon_formatting(message, tag, f":{command_name}:")

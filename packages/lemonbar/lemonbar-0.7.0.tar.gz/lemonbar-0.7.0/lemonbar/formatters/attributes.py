from enum import Enum

from lemonbar.formatters._formatter import lemon_formatting


class Modifier(str, Enum):
    STRIKETHROUGH = 'o'
    UNDERLINE = 'u'


def toggle_attribute(modifier: Modifier, message: str) -> str:
    return lemon_formatting(message, '+', modifier.value)


def set_attribute(modifier: Modifier, message: str) -> str:
    return lemon_formatting(message, '+', modifier.value)


def unset_attribute(modifier: Modifier, message: str) -> str:
    return lemon_formatting(message, '-', modifier.value)

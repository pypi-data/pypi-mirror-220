from pydantic_extra_types.color import Color

from lemonbar.formatters._formatter import make_formatter, lemon_formatting


@make_formatter('R')
def swap_background_and_foreground(message: str) -> str:
    return message


def align_left(message: str) -> str:
    return "%{l}" + message + "%{l}"


def align_center(message: str) -> str:
    return "%{c}" + message + "%{l}"


def align_right(message: str) -> str:
    return "%{r}" + message + "%{l}"


def offset_x(pixels: int, message: str) -> str:
    return lemon_formatting(message, 'O', str(pixels))


def background_color(color: Color, message: str) -> str:
    return lemon_formatting(message, 'B', str(color.as_hex()))


def foreground_color(color: Color, message: str) -> str:
    return lemon_formatting(message, 'F', str(color.as_hex()))


def underline_color(color: Color, message: str) -> str:
    return lemon_formatting(message, 'U', str(color.as_hex()))


@make_formatter('T', '-')
def reset_font(message: str) -> str:
    return message


def set_font(font_index: int, message: str) -> str:
    return lemon_formatting(message, 'T', str(font_index))

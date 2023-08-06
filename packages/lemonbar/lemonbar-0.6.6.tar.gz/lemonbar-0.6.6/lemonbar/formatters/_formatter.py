import functools
from typing import Callable, Optional


def make_formatter(tag: str, extension: Optional[str] = None):
    @functools.wraps
    def decorator(function: Callable[[...], str]) -> Callable[[...], str]:
        def formatter(*args, **kwargs):
            return lemon_formatting(function(*args, **kwargs), tag, extension)

        return formatter

    return decorator


def lemon_formatting(data: str, tag: str, extension: Optional[str] = None) -> str:
    """
    Format a string according to lemon format specified here:
        https://github.com/LemonBoy/bar#formatting
    :param data: The string to format
    :param tag: Formatting tag - present on both sides of the formatting
        %{<tag>}Message${<tag>}
    :param extension: An extension to the tag on the opening bracket
        %{<tag><extension>}Message${<tag>}
    :return: Formatted string according to the lemon spec
    """
    tag_with_extension = f'{tag}{extension or ""}'

    # f-string with {{{<var>}}} will result in {<var_data>}
    return f'%{{{tag_with_extension}}}{data}%{{{tag}}}'

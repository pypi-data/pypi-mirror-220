import screeninfo

from lemonbar.formatters._formatter import lemon_formatting, make_formatter

_TAG = 'S'


@make_formatter(_TAG, '+')
def next_monitor(message: str) -> str:
    return message


@make_formatter(_TAG, '-')
def previous_monitor(message: str) -> str:
    return message


@make_formatter(_TAG, 'f')
def first_monitor(message: str) -> str:
    return message


@make_formatter(_TAG, 'l')
def last_monitor(message: str) -> str:
    return message


def set_monitor_by_index(monitor_index: int, message: str) -> str:
    # Documentation of Lemonbar says the value must be between 0 and 9
    if monitor_index < 0 or monitor_index > 9:
        raise ValueError("The monitor index provided must be between 0 to 9")

    monitor_count = len(screeninfo.get_monitors())
    if monitor_index >= monitor_count:
        raise ValueError('The provided monitor index exceeds the amount of monitors the computer has.')

    return lemon_formatting(message, _TAG, str(monitor_index))


def set_monitor_by_name(monitor_name: str, message: str) -> str:
    monitor_names = {monitor.name for monitor in screeninfo.get_monitors()}

    if monitor_name not in monitor_names:
        raise ValueError(f"The provided monitor name \"{monitor_name}\" does not exist.")

    return lemon_formatting(message, _TAG, f'n{monitor_name}')

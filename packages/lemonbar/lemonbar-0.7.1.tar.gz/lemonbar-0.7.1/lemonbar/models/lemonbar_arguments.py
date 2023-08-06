from enum import Enum
from typing import List, Iterable, Optional, Tuple

from pydantic import BaseModel
from pydantic_extra_types.color import Color

from .bar_geometry import BarGeometry
from .bar_placement import BarPlacement
from .monitor import MonitorId


class ParameterMapping(str, Enum):
    WINDOW_GEOMETRY = 'g'
    SCREEN_OUTPUT = 'o'
    DOCK_BOTTOM = 'b'
    FORCE_DOCK = 'd'
    FONT = 'f'
    PERMANENT = 'p'
    WM_NAME = 'n'
    UNDERLINE_WIDTH = 'u'
    BACKGROUND_COLOR = 'B'
    FOREGROUND_COLOR = 'F'
    UNDERLINE_COLOR = 'U'

    def __str__(self):
        return self.value


class LemonbarArguments(BaseModel):
    geometry: Optional[BarGeometry]
    screen_outputs: List[MonitorId]
    placement: BarPlacement
    force_dock: bool
    fonts: List[str]
    permanent: bool
    wm_name: str
    underline_width: int
    underline_color: Optional[Color]
    background_color: Optional[Color]
    foreground_color: Optional[Color]

    def get_command(self) -> Tuple[str, ...]:
        command = ["lemonbar"]

        if self.placement == BarPlacement.BOTTOM:
            command.append(f'-{ParameterMapping.DOCK_BOTTOM}')

        for parameter, argument in [
            (ParameterMapping.WINDOW_GEOMETRY, self.geometry),
            (ParameterMapping.FORCE_DOCK, self.force_dock),
            (ParameterMapping.PERMANENT, self.permanent),
            (ParameterMapping.SCREEN_OUTPUT, self.screen_outputs),
            (ParameterMapping.FONT, self.fonts),
            (ParameterMapping.WM_NAME, self.wm_name),
            (ParameterMapping.UNDERLINE_WIDTH, self.underline_width),
            (ParameterMapping.UNDERLINE_COLOR, self.underline_color),
            (ParameterMapping.BACKGROUND_COLOR, self.background_color),
            (ParameterMapping.FOREGROUND_COLOR, self.foreground_color),
        ]:
            if not argument:
                continue

            if isinstance(argument, Iterable) and not isinstance(argument, BaseModel):
                for value in argument:
                    command.append(f'-{parameter}')
                    command.append(str(value))

                continue

            if isinstance(argument, Color):
                argument = argument.as_hex()

            command.append(f'-{parameter}')
            command.append(str(argument))

        return tuple(command)

    @classmethod
    def build(
            cls,
            geometry: Optional[BarGeometry],
            screen_outputs: List[str],
            placement: BarPlacement,
            force_dock: bool,
            fonts: List[str],
            permanent: bool,
            wm_name: str,
            underline_width: int,
            underline_color: Optional[Color],
            background_color: Optional[Color],
            foreground_color: Optional[Color],
    ) -> 'LemonbarArguments':
        return cls(
            geometry=geometry,
            screen_outputs=screen_outputs,
            placement=placement,
            force_dock=force_dock,
            fonts=fonts or [],
            permanent=permanent,
            wm_name=wm_name,
            underline_width=underline_width,
            underline_color=underline_color,
            background_color=background_color,
            foreground_color=foreground_color
        )

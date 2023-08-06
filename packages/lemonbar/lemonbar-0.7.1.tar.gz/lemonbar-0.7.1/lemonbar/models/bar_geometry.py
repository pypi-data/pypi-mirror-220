from typing import Optional

from pydantic import BaseModel


class BarGeometry(BaseModel):
    width: Optional[int]
    height: Optional[int]
    x_offset: Optional[int]
    y_offset: Optional[int]

    @classmethod
    def build(
            cls,
            width: Optional[int] = None,
            height: Optional[int] = None,
            x_offset: Optional[int] = None,
            y_offset: Optional[int] = None,
    ):
        return cls(
            width=width,
            height=height,
            x_offset=x_offset,
            y_offset=y_offset
        )

    def __str__(self):
        geometry = f'{self.width or ""}'

        if self.height:
            geometry += f'x{self.height}'

        if self.x_offset:
            sign = '+' if self.x_offset > 0 else '-'
            geometry += f'{sign}{self.x_offset}'

        if self.y_offset:
            sign = '+' if self.y_offset > 0 else '-'
            geometry += f'{sign}{self.y_offset}'

        return geometry

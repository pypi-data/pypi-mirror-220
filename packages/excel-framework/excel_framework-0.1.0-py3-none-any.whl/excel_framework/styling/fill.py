from dataclasses import dataclass
from overrides import override
from typing import Union
from openpyxl.cell import Cell
from openpyxl.styles import PatternFill, NamedStyle
from .color import *
from .style import StylePart


@dataclass(frozen=True)
class Fill(StylePart):
    color: Union[Color, None] = None

    @override
    def join(self, other: Union['Fill', None]) -> 'Fill':
        if other is None:
            return self
        if other.color is not None:
            return Fill(other.color)
        return self

    @override
    def apply_to(self, cell: Union[Cell, NamedStyle]) -> None:
        if self.color is not None:
            cell.fill = PatternFill(
                start_color=self.color.hex, end_color=self.color.hex, fill_type="solid")

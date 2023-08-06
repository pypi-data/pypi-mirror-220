from dataclasses import dataclass
from typing import Union
from overrides import override
from .color import *
from enum import Enum
from openpyxl.cell import Cell
import openpyxl.styles as openpyxl
from .style import StylePart


class VerticalAlignment(Enum):
    TOP = "top"
    BOTTOM = "bottom"
    CENTER = "center"


class HorizontalAlignment(Enum):
    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"


class Underline(Enum):
    single = "single"
    double = "double"


@dataclass(frozen=True)
class TextStyle(StylePart):
    font_size: Union[float, None] = None
    font_color: Union[Color, None] = None
    font_family: Union[str, None] = None
    number_format: Union[str, None] = None
    wrap_text: Union[bool, None] = None
    shrink_to_fit: Union[bool, None] = None
    horizontal_alignment: Union[HorizontalAlignment, None] = None
    vertical_alignment: Union[VerticalAlignment, None] = None
    bold: Union[bool, None] = None
    italic: Union[bool, None] = None
    underline: Union[Underline, None] = None

    @override
    def join(self, other: Union['TextStyle', None]) -> 'TextStyle':
        if other is None:
            return self
        return TextStyle(
            font_size=self.font_size if other.font_size is None else other.font_size,
            font_color=self.font_color if other.font_color is None else other.font_color,
            font_family=self.font_family if other.font_family is None else other.font_family,
            number_format=self.number_format if other.number_format is None else other.number_format,
            wrap_text=self.wrap_text if other.wrap_text is None else other.wrap_text,
            shrink_to_fit=self.shrink_to_fit if other.shrink_to_fit is None else other.shrink_to_fit,
            horizontal_alignment=self.horizontal_alignment if other.horizontal_alignment is None else other.horizontal_alignment,
            vertical_alignment=self.vertical_alignment if other.vertical_alignment is None else other.vertical_alignment,
            bold=self.bold if other.bold is None else other.bold,
            italic=self.italic if other.italic is None else other.italic,
            underline=self.underline if other.underline is None else other.underline,
        )

    @override
    def apply_to(self, cell: Union[Cell, openpyxl.NamedStyle]) -> None:
        alignment = openpyxl.Alignment()
        font = openpyxl.Font()
        font.size = self.font_size
        font.color = self.font_color if self.font_color is None else self.font_color.to_openpyxl()
        font.name = self.font_family
        cell.number_format = "" if self.number_format is None else self.number_format
        alignment.wrap_text = self.wrap_text
        alignment.shrink_to_fit = self.shrink_to_fit
        alignment.horizontal = self.horizontal_alignment.value if self.horizontal_alignment else None
        alignment.vertical = self.vertical_alignment.value if self.vertical_alignment else None
        font.bold = self.bold
        font.italic = self.italic
        font.underline = self.underline if self.underline is None else self.underline.value
        cell.alignment = alignment
        cell.font = font

from abc import ABC
from typing import Union
from dataclasses import dataclass
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import NamedStyle
from ..sizes.resizer import Resizer
from ..sizes.dimension import Dimension, ColumnDimension
from ..sizes.size import Size
from ..styling.border import ParentBorderCoordinates
from ..styling.style import Style

@dataclass
class StyleManager:
    next_style_id: int = 1

    def add_named_style(self, workbook: Workbook, style: Style) -> int:
        new_named_style = NamedStyle(f"{self.next_style_id}")
        style.apply_to(new_named_style)
        workbook.add_named_style(new_named_style)
        if style.parent_border is not None:
            for postfix in ("top", "right", "bottom", "left"):
                has_top = postfix == "top"
                has_right = postfix == "right"
                has_bottom = postfix == "bottom"
                has_left = postfix == "left"
                new_named_style = NamedStyle(f"{self.next_style_id}-{postfix}")
                style.apply_to(new_named_style)
                style.parent_border.apply_as_parent_to(new_named_style, self.next_style_id, has_top, has_right, has_bottom, has_left)
                workbook.add_named_style(new_named_style)
        self.next_style_id += 1
        return self.next_style_id - 1

@dataclass
class BuildContext(ABC):
    workbook: Workbook
    sheet: Worksheet
    resizer: Resizer
    style_manager: StyleManager
    row_index: int = 1
    column_index: int = 1
    style: Union[Style, None] = None
    style_id: Union[int, None] = None
    parent_border_coordinates: Union[ParentBorderCoordinates, None] = None

    @classmethod
    def initial(cls, title: str, dimensions: list[Dimension]) -> 'BuildContext':
        workbook = Workbook()
        workbook.active.title = title
        return BuildContext(workbook, workbook.active, Resizer(workbook.active, dimensions), StyleManager())

    def new_sheet(self, title: str, dimensions: list[Dimension]) -> 'BuildContext':
        new_sheet: Worksheet = self.workbook.create_sheet(title)
        return BuildContext(self.workbook, new_sheet, Resizer(new_sheet, dimensions), self.style_manager)

    def collect_length(self, length: int):
        self.resizer.collect_length(self.row_index, self.column_index, length)

    def collect_column_dimension(self, dimension: ColumnDimension):
        self.resizer.collect_column_dimension(dimension)

    def with_style_change(self, new_style: Union[Style, None], child_size: Size) -> 'BuildContext':
        if new_style is None:
            return self
        if self.style:
            new_style = self.style.join(new_style)
        new_parent_border_coordinates = self.parent_border_coordinates
        if new_style.parent_border:
            new_parent_border_coordinates = ParentBorderCoordinates(
                self.row_index,
                self.column_index,
                self.row_index + child_size.height - 1,
                self.column_index + child_size.width - 1
            )
        style_id = self.style_manager.add_named_style(self.workbook, new_style)
        return BuildContext(
            self.workbook,
            self.sheet,
            self.resizer,
            self.style_manager,
            self.row_index,
            self.column_index,
            new_style,
            style_id,
            new_parent_border_coordinates
        )
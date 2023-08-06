from abc import ABC
from typing import Union
from dataclasses import dataclass
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import NamedStyle
from ..sizes.resizer import Resizer
from ..sizes.dimension import Dimension, ColumnDimension
from ..styling.style import Style

@dataclass
class StyleManager:
    next_style_id: int = 1

    def add_named_style(self, workbook: Workbook, style: Style) -> str:
        style_name = str(self.next_style_id) 
        new_named_style = NamedStyle(style_name)
        style.apply_to(new_named_style)
        workbook.add_named_style(new_named_style)
        self.next_style_id += 1
        return style_name 

@dataclass
class BuildContext(ABC):
    workbook: Workbook
    sheet: Worksheet
    resizer: Resizer
    style_manager: StyleManager
    row_index: int = 1
    column_index: int = 1
    style: Union[Style, None] = None
    style_name: Union[str, None] = None
    conditional_style_names: Union[list[str], None] = None

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

    def with_style_change(self, new_style: Union[Style, None]) -> 'BuildContext':
        if new_style is None:
            return self
        if self.style:
            new_style = self.style.join(new_style)
        added_style_name = self.style_manager.add_named_style(self.workbook, new_style)
        return BuildContext(
            self.workbook,
            self.sheet,
            self.resizer,
            self.style_manager,
            self.row_index,
            self.column_index,
            new_style,
            added_style_name,
            self.conditional_style_names
        )
    
    def with_conditional_styles(self, styles: list[Style], style_names: list[str]) -> 'BuildContext':
        for style in styles:
            if self.style:
                style = self.style.join(style) 
            added_style_name = self.style_manager.add_named_style(self.workbook, style)
            style_names.append(added_style_name)
        return BuildContext(
            self.workbook,
            self.sheet,
            self.resizer,
            self.style_manager,
            self.row_index,
            self.column_index,
            self.style,
            self.style_name,
            style_names
        )
        
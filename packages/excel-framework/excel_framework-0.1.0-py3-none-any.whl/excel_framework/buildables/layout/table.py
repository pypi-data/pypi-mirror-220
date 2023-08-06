from ...internals.buildable import Buildable
from overrides import override
from dataclasses import dataclass
from typing import Generic, TypeVar, Callable, Any, Union
from .column import Column
from .row import Row
from ..non_layout.excel_cell import ExcelCell
from ...styling.style import Style
from ...styling.styler import Styler
from ...internals.build_context import BuildContext
from ...sizes.dimension import ColumnDimension, AutoWidth, FixedWidth

T = TypeVar("T")


@dataclass(frozen=True)
class TableColumn(Generic[T]):
    name: str
    value: Callable[[T], Any]
    width: Union[AutoWidth, FixedWidth, None] = None
    column_name_style: Union[Style, None] = None
    value_style: Union[Callable[[T], Union[int, None]], None] = None


@dataclass(frozen=True)
class Table(Buildable, Generic[T]):
    columns: list[TableColumn[T]]
    data: list[T]
    column_name_style: Union[Style, None] = None
    data_style: Union[Style, None] = None
    value_styles: Union[list[Union[Style, int]], None] = None

    @override
    def internal_build(self, context: BuildContext) -> None:
        for i, column in enumerate(self.columns):
            if column.width:
                context.collect_column_dimension(
                    ColumnDimension(context.column_index + i, column.width)
                )
        if self.value_styles:
            joined_data_style = self.data_style
            if context.style:
                joined_data_style = context.style.join(self.data_style)
            for i,value_style in enumerate(self.value_styles):
                assert type(value_style) is Style
                joined_style = value_style
                if joined_data_style:
                    joined_style = joined_data_style.join(value_style)
                style_id = context.style_manager.add_named_style(context.workbook, joined_style)
                self.value_styles[i] = style_id
        self.build().internal_build(context)

    @override
    def build(self) -> 'Buildable':
        return Column([
            Styler(
                Row(children=self.__get_column_name_cells()),
                self.column_name_style
            ),
            Styler(
                Column(children=self.__get_value_rows()),
                self.data_style
            )
        ])

    def __get_column_name_cells(self) -> list[Buildable]:
        excel_cells: list[Buildable] = []
        for column in self.columns:
            excel_cells.append(
                Styler(
                    ExcelCell(column.name),
                    column.column_name_style
                )
            )
        return excel_cells

    def __get_value_rows(self) -> list[Buildable]:
        rows: list[Buildable] = []
        for model in self.data:
            excel_cells = []
            for column in self.columns:
                value = column.value(model)
                style_id: Union[int, None] = None
                style_index = column.value_style(
                    model) if column.value_style else None
                if style_index is not None:
                    style_id = self.value_styles[style_index] # type: ignore
                excel_cells.append(ExcelCell(value, style_id))
            rows.append(Row(children=excel_cells))
        return rows
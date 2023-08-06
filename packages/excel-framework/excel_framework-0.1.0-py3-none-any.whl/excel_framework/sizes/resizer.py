from openpyxl.worksheet.worksheet import Worksheet
from typing import Union
from openpyxl.utils import get_column_letter
from .dimension import ColumnDimension, RowDimension, Dimension, FixedInternalDimension, InternalDimension


class Resizer:
    def __init__(self, sheet: Worksheet, dimensions: list[Dimension]) -> None:
        self.sheet = sheet
        self.row_dimensions = dict[Union[int, None], FixedInternalDimension]()
        self.column_dimensions = dict[Union[int,
                                            None], InternalDimension]()
        for dimension in dimensions:
            if isinstance(dimension, RowDimension):
                self.row_dimensions[dimension.index] = dimension.to_internal()
            elif isinstance(dimension, ColumnDimension):
                self.column_dimensions[dimension.index] = dimension.to_internal(
                )

    def collect_length(self, row_index: int, column_index: int, length: int) -> None:
        if row_index not in self.row_dimensions and None in self.row_dimensions:
            self.row_dimensions[row_index] = self.row_dimensions[None]
        if column_index in self.column_dimensions:
            dimension = self.column_dimensions[column_index]
            self.column_dimensions[column_index] = dimension.with_length(
                length)
        elif None in self.column_dimensions:
            dimension = self.column_dimensions[None]
            self.column_dimensions[column_index] = dimension.with_length(
                length)

    def collect_column_dimension(self, dimension: ColumnDimension):
        self.column_dimensions[dimension.index] = dimension.to_internal()

    def resize(self):
        self.__resize_rows()
        self.__resize_columns()

    def __resize_rows(self):
        if None in self.row_dimensions:
            del self.row_dimensions[None]
        for row_index in self.row_dimensions:
            self.sheet.row_dimensions[row_index].height = self.row_dimensions[row_index].final_value()

    def __resize_columns(self):
        if None in self.column_dimensions:
            del self.column_dimensions[None]
        for col_index in self.column_dimensions:
            assert(type(col_index) is int)
            column_dimension = self.column_dimensions[col_index]
            column_letter = get_column_letter(col_index)
            self.sheet.column_dimensions[column_letter].width = column_dimension.final_value()

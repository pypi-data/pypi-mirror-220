from dataclasses import dataclass
from typing import Any
from ...internals.buildable import Buildable
from ...internals.build_context import BuildContext
from ...sizes.size import Size
from overrides import override
from typing import Union


@dataclass(frozen=True)
class ExcelCell(Buildable):
    value: Any = None
    style_id: Union[int, None] = None

    def __get_length(self):
        if self.value is None:
            return 0
        if str(self.value).startswith('='):
            return 0
        return len(str(self.value))

    @override
    def get_size(self) -> Size:
        return Size(1, 1)

    @override
    def internal_build(self, context: BuildContext) -> None:
        context.collect_length(self.__get_length())
        cell = context.sheet.cell(
            context.row_index, context.column_index, self.value)
        if not self.style_id and not context.style:
            return
        style_id = self.style_id if self.style_id is not None else context.style_id
        assert style_id is not None
        if context.style and context.style.parent_border:
            assert context.parent_border_coordinates is not None
            has_top = cell.row == context.parent_border_coordinates.row_left_top
            has_right = cell.column == context.parent_border_coordinates.col_right_bottom
            has_bottom = cell.column == context.parent_border_coordinates.row_right_bottom
            has_left = cell.column == context.parent_border_coordinates.col_left_top
            context.style.apply_to(cell)
            assert context.style_id is not None
            context.style.parent_border.apply_as_parent_to(cell, style_id, has_top, has_right, has_bottom, has_left)
        elif context.style:
            cell.style = f"{style_id}"

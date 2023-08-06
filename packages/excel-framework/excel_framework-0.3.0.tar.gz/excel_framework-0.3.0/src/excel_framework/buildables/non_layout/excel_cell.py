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
    conditional_style_index: Union[int, None] = None

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
        if not self.conditional_style_index and not context.style:
            return
        style_name = context.style_name
        if self.conditional_style_index is not None:
            assert context.conditional_style_names is not None
            style_name = context.conditional_style_names[self.conditional_style_index]
        cell.style = style_name

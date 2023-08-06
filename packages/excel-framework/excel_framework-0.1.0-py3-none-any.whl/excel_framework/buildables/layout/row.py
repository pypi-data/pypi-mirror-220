from ...internals.buildable import Buildable
from ...internals.build_context import BuildContext
from ...sizes.size import Size
from overrides import override

class Row(Buildable):
    def __init__(self, children: list[Buildable] = []) -> None:
        self.children = children
        super().__init__()

    @override
    def get_size(self) -> Size:
        width = 0
        height = 0
        for child in self.children:
            child_size = child.get_size()
            width += child_size.width
            if child_size.height > height:
                height = child_size.height
        return Size(width, height)

    @override
    def internal_build(self, context: BuildContext) -> None:
        row_index = context.row_index
        column_index = context.column_index
        for child in self.children:
            child_size = child.get_size()
            child.internal_build(context)
            column_index += child_size.width
            context.column_index = column_index
            context.row_index = row_index




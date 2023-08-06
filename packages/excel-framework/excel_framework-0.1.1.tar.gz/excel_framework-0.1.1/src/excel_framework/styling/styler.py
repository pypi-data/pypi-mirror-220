from dataclasses import dataclass
from typing import Union
from overrides import override
from ..internals.buildable import Buildable
from ..internals.build_context import BuildContext
from .style import Style


@dataclass(frozen=True)
class Styler(Buildable):
    child: Buildable
    style: Union[Style, None] = None

    @override
    def internal_build(self, context: BuildContext) -> None:
        new_context = context.with_style_change(
            self.style, self.child.get_size())
        self.child.internal_build(new_context)

    @override
    def build(self) -> 'Buildable':
        return self.child
from dataclasses import dataclass
from typing import Union
from overrides import override

from ..internals.buildable import Buildable
from ..internals.build_context import BuildContext
from .style import Style

@dataclass
class StyleName:
    name: Union[str, None] = None

@dataclass(frozen=True)
class Styler(Buildable):
    child: Buildable
    style: Union[Style, None] = None
    style_name: Union[StyleName, None] = None

    @override
    def internal_build(self, context: BuildContext) -> None:
        new_context = context.with_style_change(self.style)
        if self.style_name is not None:
            self.style_name.name = new_context.style_name
        self.child.internal_build(new_context)

    @override
    def build(self) -> 'Buildable':
        return self.child

@dataclass(frozen=True)
class ConditionalStyler(Buildable):
    child: Buildable
    styles: list[Style]
    style_names: list[str]

    @override
    def internal_build(self, context: BuildContext) -> None:
        if len(self.styles) == 0:
            return self.child.internal_build(context)
        new_context = context.with_conditional_styles(self.styles, self.style_names)
        return self.child.internal_build(new_context)

    @override
    def build(self) -> Buildable:
        return self.child
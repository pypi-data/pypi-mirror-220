from abc import ABC
from overrides import EnforceOverrides
from ..sizes.size import Size
from .build_context import BuildContext


class Buildable(ABC, EnforceOverrides):
    def build(self) -> 'Buildable':
        return self

    def internal_build(self, context: BuildContext) -> None:
        if self.build() == self:
            raise Exception(
                f"Error: build method not defined: The class {self.__class__.__name__,} failed to override the build method")
        self.build().internal_build(context)

    def get_size(self) -> Size:
        if self.build() == self:
            raise Exception(
                f"Error: build method not defined: The class {self.__class__.__name__,} failed to override the build method")
        return self.build().get_size()

from dataclasses import dataclass
from overrides import override
from abc import ABC, abstractmethod
from typing import Union


@dataclass(frozen=True)
class FixedWidth:
    width: float


@dataclass(frozen=True)
class AutoWidth:
    min_width: float = 13
    max_width: Union[float, None] = None
    length_multiplier: float = 1


class InternalDimension(ABC):
    @abstractmethod
    def with_length(self, length: int) -> 'InternalDimension':
        pass

    @abstractmethod
    def final_value(self) -> float:
        pass


@dataclass(frozen=True)
class FixedInternalDimension(InternalDimension):
    value: float

    @override
    def with_length(self, length: int) -> 'FixedInternalDimension':
        return self

    @override
    def final_value(self) -> float:
        return self.value


@dataclass(frozen=True)
class VariableInternalDimension(InternalDimension):
    auto_width: AutoWidth
    required_length: int = 0

    @override
    def with_length(self, length: int) -> 'VariableInternalDimension':
        return VariableInternalDimension(
            self.auto_width,
            length if length > self.required_length else self.required_length
        )

    @override
    def final_value(self) -> float:
        proposed_value = self.required_length*self.auto_width.length_multiplier
        if self.auto_width.min_width > proposed_value:
            return self.auto_width.min_width
        if self.auto_width.max_width is not None and self.auto_width.max_width < proposed_value:
            return self.auto_width.max_width
        return proposed_value


@dataclass(frozen=True)
class Dimension(ABC):
    index: Union[int, None]

    @abstractmethod
    def to_internal(self):
        pass


@dataclass(frozen=True)
class RowDimension(Dimension):
    """
    If the given index is None, the dimension will be applied onto all rows
    """
    height: float = 15

    @override
    def to_internal(self) -> FixedInternalDimension:
        return FixedInternalDimension(self.height)


@dataclass(frozen=True)
class ColumnDimension(Dimension):
    width: Union[FixedWidth, AutoWidth]

    @override
    def to_internal(self):
        if type(self.width) is FixedWidth:
            return FixedInternalDimension(self.width.width)
        else:
            assert type(self.width) is AutoWidth
            return VariableInternalDimension(self.width)

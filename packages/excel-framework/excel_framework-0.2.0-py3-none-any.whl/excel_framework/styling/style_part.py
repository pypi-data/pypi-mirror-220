from abc import ABC, abstractmethod
from typing import Union
from openpyxl.cell import Cell


class StylePart(ABC):
    @abstractmethod
    def join(self, other: Union['StylePart', None]) -> 'StylePart':
        pass

    @abstractmethod
    def apply_to(self, cell: Cell) -> None:
        pass

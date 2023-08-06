from dataclasses import dataclass, field
from typing import Union
from ..sizes.dimension import Dimension
from ..internals.buildable import Buildable


@dataclass(frozen=True)
class ExcelSheet:
    title: str
    child: Union[Buildable, None] = None
    dimensions: list[Dimension] = field(default_factory=list)

from typing import Union
from dataclasses import dataclass, field
from .excel_sheet import ExcelSheet
from ..styling.styler import Styler
from ..styling.style import Style
from ..internals.build_context import BuildContext


@dataclass(frozen=True)
class ExcelFile:
    filename: str
    sheets: list[ExcelSheet] = field(default_factory=list)
    global_style: Union[Style, None] = None

    def create(self):
        if len(self.sheets) == 0:
            return
        context = BuildContext.initial(
            self.sheets[0].title, self.sheets[0].dimensions)
        for i, sheet in enumerate(self.sheets):
            if i > 0:
                context = context.new_sheet(sheet.title, sheet.dimensions)
            if sheet.child and self.global_style:
                Styler(
                    sheet.child, self.global_style).internal_build(context)
            elif sheet.child:
                sheet.child.internal_build(context)
            context.resizer.resize()
        context.workbook.save(self.filename)

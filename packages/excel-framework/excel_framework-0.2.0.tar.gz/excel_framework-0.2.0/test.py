from src.excel_framework import ExcelFile, ExcelSheet, Table, AutoWidth, Style, Fill, Colors, BorderSide, BorderStyle, TableColumn, Border, ConditionalStyle, TextStyle
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import PatternFill, Side, NamedStyle
columns: list[TableColumn[list[str]]] = []
for i in range(11):
    columns.append(TableColumn(str(i), lambda item, i=i: item[i], AutoWidth()))
columns.append(TableColumn[list[str]](str(11), lambda item: item[11], AutoWidth(),value_style=Style(text_style=TextStyle(bold=True)), conditional_style=ConditionalStyle([Style(fill=Fill(Colors.red))], lambda _: 0)))


data: list[list[str]] = []
for i in range(16000):
    row: list[str] = []
    for j in range(12):
        row.append(f"i: {i}, j: {j}")
    data.append(row)
import time
start = time.time() * 1000
ExcelFile("testfile.xlsx", sheets=[
    ExcelSheet("Ordersheet", child=Table[list[str]](
        columns=columns,
        data=data,
        data_style=Style(fill=Fill(color=Colors.white), child_border=Border(all=BorderSide(border_style=BorderStyle.THICK))),
    ))
]).create()
end = time.time() * 1000
print(f"framework needed {end - start}ms") 
from openpyxl import load_workbook, Workbook
from copy import copy  # fillコピーに必要

file_path = "C:/Users/1109685/Documents/IR/Sample_freejob.xlsx"
wb_src = load_workbook(file_path)
ws_src = wb_src.worksheets[0]

wb_new = Workbook()
ws_new = wb_new.active
ws_new.title = ws_src.title

max_col = ws_src.max_column

for row in range(1, 64):
    for col in range(1, max_col + 1):
        src_cell = ws_src.cell(row=row, column=col)
        new_cell = ws_new.cell(row=row, column=col)

        # 値をコピー
        new_cell.value = src_cell.value

        # 背景塗りつぶし（fill）をコピー（浅いコピーを推奨）
        if src_cell.fill is not None:
            new_cell.fill = copy(src_cell.fill)

# 保存
output_path = "C:/Users/1109685/Documents/IR/Sample_freejob_short.xlsx"
wb_new.save(output_path)

from openpyxl import load_workbook, Workbook

file_path = "C:/Users/1109685/Documents/IR/Sample_freejob.xlsx"
wb_src = load_workbook(file_path)
ws_src = wb_src.worksheets[0]

wb_new = Workbook()
ws_new = wb_new.active
ws_new.title = ws_src.title

# 最大列数を取得
max_col = ws_src.max_column

# 1〜63行を新しいシートにコピー
for row in range(1, 64):
    for col in range(1, max_col + 1):
        ws_new.cell(row=row, column=col).value = ws_src.cell(row=row, column=col).value

# 保存
output_path = "C:/Users/1109685/Documents/IR/Sample_freejob_top63.xlsx"
wb_new.save(output_path)

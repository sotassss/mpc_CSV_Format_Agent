import pandas as pd

# 入出力ファイル
excel_path = 'C:/Users/1109685/Documents/IR/input/freejob/Sample_freejob_short_format.xlsx'
csv_path = 'C:/Users/1109685/Documents/IR/input/sample/freejob.csv'

df = pd.read_excel(excel_path)
df.to_csv(csv_path, index=False, encoding='utf-8-sig')  

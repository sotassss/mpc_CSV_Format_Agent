import pandas as pd
import numpy as np

# 入力・出力ファイルパス
input_excel = "C:/Users/1109685/Documents/IR/Sample_freejob_short.xlsx"
output_excel = "C:/Users/1109685/Documents/IR/Sample_freejob_short_format.xlsx"

# Excelファイルを読み込み
df = pd.read_excel(input_excel)

# 空白・空文字セルをNaNに置換
df = df.replace(r'^\s*$', np.nan, regex=True)

# すべてのセルがNaNまたは'nan'含む文字列なら削除する関数
def is_all_nan_or_contains_nan_string(col):
    for v in col:
        if pd.isna(v):
            continue
        s = str(v).lower()
        if 'nan' not in s:
            return False
    return True

# 削除対象列の抽出と削除
cols_to_drop = [col for col in df.columns if is_all_nan_or_contains_nan_string(df[col])]
df = df.drop(columns=cols_to_drop)

print(f"最終DataFrameのshape: {df.shape}")

# Excelに保存
df.to_excel(output_excel, index=False)
print(f"最終Excelファイルを {output_excel} に保存しました。")

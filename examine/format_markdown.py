import re
import pandas as pd
import io
import numpy as np

def is_separator_line(line: str) -> bool:
    pattern = r'^[-:\s|]+$'
    return bool(re.match(pattern, line.strip()))

input_markdown = "output/data_output_color_short.md"
output_markdown = "output/data_output_color_short_modified.md"

with open(input_markdown, "r", encoding="utf-8") as f:
    lines = f.readlines()

filtered_lines = [line for line in lines if line.strip() and not is_separator_line(line)]
filtered_lines = [line.strip().strip('|') for line in filtered_lines]
cleaned_markdown = '\n'.join(filtered_lines)

df = pd.read_csv(io.StringIO(cleaned_markdown), sep='|', skipinitialspace=True)

# 空白・空文字セルをNaNに置換
df = df.replace(r'^\s*$', np.nan, regex=True)

# 全てのセルがNaNまたは'nan'含む文字列なら削除する関数
def is_all_nan_or_contains_nan_string(col):
    for v in col:
        if pd.isna(v):
            continue
        s = str(v).lower()
        if 'nan' not in s:
            return False
    return True

cols_to_drop = [col for col in df.columns if is_all_nan_or_contains_nan_string(df[col])]
df = df.drop(columns=cols_to_drop)

print(f"最終DataFrameのshape: {df.shape}")

output_md = df.to_markdown(index=False)
with open(output_markdown, "w", encoding="utf-8") as f:
    f.write(output_md)

print(f"最終Markdownテーブルを{output_markdown}に保存しました。")

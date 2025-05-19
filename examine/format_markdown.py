import pandas as pd
import io

input_markdown = "output/data_output_color_short.md"
output_markdown = "output/data_output_color_short_modified.md"

# Markdownファイルを読み込む
with open(input_markdown, "r", encoding="utf-8") as f:
    markdown_text = f.read()

# 各行の先頭・末尾のパイプを削除し、空行を除去
lines = [line.strip().strip('|') for line in markdown_text.strip().split('\n') if line.strip()]
cleaned_markdown = '\n'.join(lines)

# DataFrameに変換
df = pd.read_csv(io.StringIO(cleaned_markdown), sep='|')

# 全てNaNの列を削除
df = df.dropna(how='all', axis=1)

# DataFrameをMarkdown形式に変換
output_md = df.to_markdown(index=False)

# Markdownファイルとして保存
with open(output_markdown, "w", encoding="utf-8") as f:
    f.write(output_md)

print(f"Markdownテーブルを{output_markdown}に保存しました。")

import pandas as pd
import sqlite3

# Excel読み込み
df = pd.read_excel("C:/Users/1109685/Documents/IR/Sample_freejob_short.xlsx")


# SQLiteに接続（存在しなければ新規作成）
conn = sqlite3.connect("my_data.db")

# DataFrameをSQLiteのテーブルに保存（既存テーブルは上書き）
df.to_sql("my_table", conn, if_exists="replace", index=False)

# 接続を閉じる
conn.close()

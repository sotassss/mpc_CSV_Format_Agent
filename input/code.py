import pandas as pd

# データファイルのパス
file_path = 'C:/Users/1109685/Documents/IR/input/sample.csv'

# CSVファイルを読み込む
try:
    df = pd.read_csv(file_path)
except Exception as e:
    print(f'Error reading the CSV file: {e}')
    exit()

# 電話番号のフォーマットを統一する関数
def format_phone_number(phone):
    return phone.replace('-', '')

# 電話番号のフォーマットを統一
df['電話番号'] = df['電話番号'].apply(format_phone_number)

# 結果をCSVファイルに上書き保存
try:
    df.to_csv(file_path, index=False)
except Exception as e:
    print(f'Error saving the CSV file: {e}')
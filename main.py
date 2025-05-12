import os
from datetime import datetime
from langchain_openai import ChatOpenAI
from src.nodes.code_execution import ExecutedResult
from src.agent import ExcelFormat
from dotenv import load_dotenv

def main():
    load_dotenv()

    input_data = r"C:\Users\1109685\Documents\IR\input\sample.csv"

    # 現在時刻を取得してフォルダ・ファイル名を生成
    now = datetime.now()
    date_str = now.strftime("%m_%d")
    datetime_str = now.strftime("%m%d_%H%M")

    output_dir = f"output_{date_str}"
    output_filename = f"result_{datetime_str}.csv"
    output_path = os.path.join(output_dir, output_filename)

    # LLMとAgentの初期化
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
    agent = ExcelFormat(llm)
    output = agent.run(input_data)

    # 出力を文字列に変換
    if isinstance(output, ExecutedResult):
        output_str = f"実行結果: {output.result}\nエラー内容: {output.error}"
    else:
        output_str = str(output)

    # 出力フォルダが存在しない場合は作成
    os.makedirs(output_dir, exist_ok=True)

    # 結果を保存
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output_str)

    print(f"出力結果を {output_path} に保存しました。")

if __name__ == "__main__":
    main()

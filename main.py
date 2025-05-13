import os
from datetime import datetime
from langchain_openai import ChatOpenAI
from src.agent import ExcelFormat
from dotenv import load_dotenv

def main():
    load_dotenv()

    # input_data = r"C:\Users\1109685\Documents\IR\input\sample_mess.csv"
    input_data = r"C:\Users\1109685\Documents\IR\input\sample.csv"

    # 現在時刻を取得してフォルダ・ファイル名を生成
    now = datetime.now()
    date_str = now.strftime("%m_%d")
    datetime_str = now.strftime("%m%d_%H%M")

    output_dir = os.path.join("output", f"output_{date_str}")
    output_filename = f"result_{datetime_str}.csv"
    output_path = os.path.join(output_dir, output_filename)

    # LLMとAgentの初期化
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
    agent = ExcelFormat(llm,maximum_iteration=3)
    result = agent.run(input_data)
    output_str = result['generated_code'].output

    # 出力フォルダが存在しない場合は作成
    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "w", newline='', encoding="utf-8") as f:
        f.write(output_str)

    print(f"出力結果を {output_path} に保存しました。")

if __name__ == "__main__":
    main()

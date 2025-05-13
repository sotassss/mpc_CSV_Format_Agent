import os
from datetime import datetime
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from src.agent import ExcelFormat
from src.utils.generate_output_path import generate_output_path

def main():
    load_dotenv()

    # input_data = r"C:\Users\1109685\Documents\IR\input\sample_mess.csv"
    input_data = r"C:\Users\1109685\Documents\IR\input\sample.csv"

    # LLMとAgentの初期化
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
    agent = ExcelFormat(llm,maximum_iteration=3)
    result = agent.run(input_data)
    output_str = result['generated_code'].output

    # 出力ファイルパス作成
    output_path=generate_output_path()
    with open(output_path, "w", newline='', encoding="utf-8") as f:
        f.write(output_str)

    print(f"出力結果を {output_path} に保存しました。")

if __name__ == "__main__":
    main()

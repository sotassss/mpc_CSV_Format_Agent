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
    
    format_data_path = agent.run(input_data)

    print(f"出力結果を {format_data_path} に保存しました。")

if __name__ == "__main__":
    main()

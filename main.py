from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from src.agent import ExcelFormat

def main():
    load_dotenv()

    # 解析ファイル
    # input_data = "C:/Users/1109685/Documents/IR/input/sample_mess.csv"
    input_data = "C:/Users/1109685/Documents/IR/input/sample.csv"

    # LLMとAgentの初期化
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
    agent = ExcelFormat(llm,maximum_iteration=3)
    
    # Agentの実行
    format_data_path = agent.run(input_data)

    print(f"出力結果を {format_data_path} に保存しました。")

if __name__ == "__main__":
    main()

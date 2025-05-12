from langchain_core.prompts import ChatPromptTemplate
from src.model_types import DataAnalysisResult,GeneratedCode, ExecutedResult

class CodeExecutionNode:
    def __init__(self, llm):
        self.llm = llm.with_structured_output(ExecutedResult)

    def run(self, data: DataAnalysisResult, generated_code: GeneratedCode) -> ExecutedResult:
        prompt = ChatPromptTemplate.from_messages([
            ("system",
            "あなたの業務は与えられたデータとPythonコードから、Pythonコードの実行結果を得ることです。"),
            ("human",
            "以下のデータとPythonコードから、Pythonコード実行結果を出力してください。\n\n"
            "データ: {data}\n\n"
            "Pythonコード: {generated_code}\n\n"
            "実行結果のCSVファイルのみを出力してください。")
        ])

        chain = prompt | self.llm
        result = chain.invoke({
            "data": data.data_content,
            "generated_code": generated_code.code
        })
        
        print("LLM 出力:", result)  # デバッグのために出力内容を確認
        
        return result  # 実行結果をそのまま返す

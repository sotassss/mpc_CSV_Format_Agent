from langchain_core.prompts import ChatPromptTemplate

from src.model_types import DataAnalysisResult

class DataAnalysisNode:
    def __init__(self,llm):
        self.llm=llm.with_structured_output(DataAnalysisResult)

    def run(self, data: str) -> DataAnalysisResult:
        with open(data, encoding="utf-8") as f:
            data = f.read()
        prompt = ChatPromptTemplate.from_messages([
            ("system",
            "あなたは優秀なデータ分析者です。あなたの業務はデータを分析し、内容をまとめることです。"),
            ("human",
            "以下のデータの概要を説明してください。\n\n"
            "データ:\n{data}\n\n"
            "ヘッダー情報、行数、列数などを理解してください。\n\n")
        ])

        chain = prompt | self.llm
        return chain.invoke({"data": data})

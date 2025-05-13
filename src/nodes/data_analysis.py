import pandas as pd
from langchain_core.prompts import ChatPromptTemplate

from src.model_types import DataAnalysisResult

class DataAnalysisNode:
    def __init__(self, llm):
        self.llm = llm.with_structured_output(DataAnalysisResult)

    def run(self, data: str) -> DataAnalysisResult:
        # DataFrameの読み込み
        data_df = pd.read_csv(data, encoding="utf-8")
        data_content_str = data_df.to_csv(index=False, encoding="utf-8")

        prompt = ChatPromptTemplate.from_messages([
            ("system", "あなたは優秀なデータ分析者です。あなたの業務はデータを分析し、内容をまとめることです。"),
            ("human", "以下のデータの概要を説明してください。\n\n"
                       "データ:\n{data}\n\n"
                       "ヘッダー情報、行数、列数などを理解してください。\n\n")
        ])

        chain = prompt | self.llm
        result = chain.invoke({"data": data_content_str})

        return DataAnalysisResult(
            data_summary=result.data_summary,  
            data_content=data_content_str  
        )

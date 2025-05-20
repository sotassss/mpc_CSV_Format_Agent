import pandas as pd
from langchain_core.prompts import ChatPromptTemplate

from src.model_types import SearchProblem

class SearchProblemNode:
    def __init__(self, llm):
        self.llm = llm.with_structured_output(SearchProblem)

    def run(self, data: str) -> SearchProblem:
        # DataFrameの読み込み
        data_df = pd.read_csv(data, encoding="utf-8")
        data_content_str = data_df.to_csv(index=False, encoding="utf-8")

        prompt = ChatPromptTemplate.from_messages([
            ("system", "あなたは優秀なデータ分析者です。あなたの業務はデータを分析し、要求に応じた正確な回答を生成することです。"),
            ("human", """
                    目的はtidyデータを生成することです。
                    以下のデータを解析し、tidyデータを生成する上での問題点を3つまで上げてください。
                    入力データ:{data}
                    
                    注意点:
                    - 何が問題なのかを明確に指定すること。
                    - 複数問題がある場合でも、とくに重要度が高いと思われるものを1つ具体的に上げること。                   
                    """
            ),
        ])

        chain = prompt | self.llm
        result = chain.invoke({"data": data_content_str})

        return result

from langchain_core.prompts import ChatPromptTemplate

from src.model_types import ExecutePython,EvaluationData

class ResultEvaluationNode:
    def __init__(self,llm):
        self.llm=llm.with_structured_output(EvaluationData)

    def run(self, executed_data:ExecutePython) -> EvaluationData:
        prompt = ChatPromptTemplate.from_messages([
            ("system",
            "あなたはデータの評価者です。"),
            ("human",
             """
            以下のデータがtidyデータであるかを判断してください。
            データ:{executed_data}

            tidyデータでない場合のフィードバックも作成してください。
            """)
        ])

        chain = prompt | self.llm
        result= chain.invoke({"executed_data":executed_data})
        return result
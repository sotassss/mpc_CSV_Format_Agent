from langchain_core.prompts import ChatPromptTemplate

from src.model_types import ExecutedResult,EvaluationResult

class ResultEvaluationNode:
    def __init__(self,llm):
        self.llm=llm.with_structured_output(EvaluationResult)

    def run(self, data: str, executed_result:ExecutedResult) -> EvaluationResult:
        prompt = ChatPromptTemplate.from_messages([
            ("system",
            "あなたはデータの評価者です。"),
            ("human",
            "以下のデータが正確に成形されているかを分析してください。\n\n"
            "元データ:\n{data}\n\n"
            "成形後データ：{executed_result}\n\n")
        ])

        chain = prompt | self.llm
        return chain.invoke({
            "data": data,
            "executed_result": executed_result.result 
        })

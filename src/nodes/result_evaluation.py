from langchain_core.prompts import ChatPromptTemplate

from src.model_types import EvaluationResult,GeneratedCode,DataAnalysisResult

class ResultEvaluationNode:
    def __init__(self,llm):
        self.llm=llm.with_structured_output(EvaluationResult)

    def run(self, data_original:DataAnalysisResult, data_formatted:GeneratedCode) -> EvaluationResult:
        prompt = ChatPromptTemplate.from_messages([
            ("system",
            "あなたはデータの評価者です。"),
            ("human",
            "以下のデータが正確に「成形」されているかを分析してください。\n\n"
            "成形前データ:{data_original}\n\n"
            "成形後データ：{data_formatted}\n\n"
            "注意点：\n"
            "1. 成形後はすべてのデータを含む必要はない。\n"
            "2. 文脈上の構造が保存できている\n"
            "3. 成形後データがエラーとなっている場合は再度やり直す。\n\n")
        ])

        chain = prompt | self.llm
        return chain.invoke({
            "data_original": data_original.data_content,
            "data_formatted": data_formatted.output 
        })

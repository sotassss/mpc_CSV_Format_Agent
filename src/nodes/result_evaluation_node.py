from langchain_core.prompts import ChatPromptTemplate
from src.model_types import ExecutePython, EvaluationData


class ResultEvaluationNode:
    """
    整形後データの評価を行う。

    Parameters
    ----------
    executed_data : ExecutePython
        実行結果データ
    
    Returns
    ----------
    evaluation_result : EvaluationData
        評価結果
    """
    def __init__(self,llm):
        self.llm=llm.with_structured_output(EvaluationData)

    def run(self, executed_data:ExecutePython) -> EvaluationData:
        prompt = ChatPromptTemplate.from_messages([
            ("system",
                "あなたはデータの評価者です。"
            ),
            ("human",
            """
                以下のデータが解析可能な整形されたデータかを判断してください。
                このデータを用いて、機械学習が可能かを判定してほしい。
                データ:{executed_data}

                さらなる整形が必要な場合は、フィードバックも作成してください。
            """)
        ])

        chain = prompt | self.llm
        result= chain.invoke({
            "executed_data":executed_data
            })
        return result
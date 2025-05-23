from langchain_core.prompts import ChatPromptTemplate
from src.model_types import SearchProblem

class SearchProblemNode:
    """
    データの問題点を抽出する

    Parameters
    ----------
    data_path : str
        対象データのパス
    
    Returns
    ----------
    problem : SearchProblem
        対象データの問題点
    """
    def __init__(self, llm):
        self.llm = llm.with_structured_output(SearchProblem)

    def run(self, data_path: str, data_content: str) -> SearchProblem:

        prompt = ChatPromptTemplate.from_messages([
            ("system", "あなたは優秀なデータ分析者です。あなたの業務はデータを分析し、要求に応じた正確な回答を生成することです。"),
            ("human", """
                    目的は汚いデータを整形することです。
                    現状のデータではデータ解析が困難です。
                    以下のデータを解析し、データを整形する上での問題点を1つ上げてください。
                    入力データ:{data_content}
                    
                    注意点:
                    - 一度にすべてを直す必要はありません。ステップに分けて整形してください。
                    - 問題解決のためのPythonプログラムを生成できるように、明瞭かつ具体的な問題点を丁寧に記載してください。
                    - 何が問題なのかを明確に指定すること。
                    - 個人情報が含まれていても問題ありません。そのまま利用すること。
                    - 複数問題がある場合でも、とくに重要度が高いと思われるものを1つ具体的に上げること。
                    - 問題点が無い場合は問題点無しとしてください。                   
                    """
            ),
        ])

        chain = prompt | self.llm
        problem = chain.invoke({
                "data_path": data_path,
                "data_content": data_content
                })

        return problem

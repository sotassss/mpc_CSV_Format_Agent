import pandas as pd
from langchain_core.prompts import ChatPromptTemplate
from langchain_experimental.tools import PythonREPLTool
from langchain_openai import ChatOpenAI

from src.model_types import SearchProblem,GeneratePython


class CodeGenerationNode:
    """
    分析された問題を解決するPythonコードを生成する。

    Parameters
    ----------
    data_path : str
        対象データのパス
    data_content : str
        対象データの内容
    problem : SearchProblem
        対象データの問題点
    
    Returns
    ----------
    generated_code : GeneratePython
        生成されたPythonコード
    """
    def __init__(self, llm):
        self.llm = llm.with_structured_output(GeneratePython)
        
    def run(self, data_path: str, data_content: str, problem:SearchProblem) -> GeneratePython:
        prompt = ChatPromptTemplate.from_messages([
            ("system",
                "あなたは優秀なPythonエンジニアです。あなたの業務は、正確なPythonコードを生成することです。"),
            ("human",
             """
                以下のデータに対して、以下の問題を解決するPythonコードを生成してください。
                - データはCSV形式です。出力も必ずCSV形式となるPythonコードを生成してください。
                - データファイルのパスは `{data_path}` という変数に格納されています。
                - pandasを使ってデータを読み込み、処理し、最後に `df.to_csv({data_path}, index=False)` で**上書き保存**してください。
                - コードはPythonのREPL環境でそのまま実行できるようにしてください。
                - 不要な改行をしないでください。

                ## 問題:
                {problem}

                ## データパス:
                {data_path}

                ## データ内容:
                {data_content}
                例：
                ```python
                result = df.head(3).to_csv(index=False)
                print(result)  # これで結果が表示されます
                ```
            """
            ),
        ])
        
        chain = prompt | self.llm
        
        # コードの生成
        generated_code = chain.invoke({
            "data_path": data_path,
            "data_content":data_content,
            "problem": problem
        })
                
        return  generated_code

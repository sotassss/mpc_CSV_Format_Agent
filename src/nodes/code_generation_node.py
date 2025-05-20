from langchain_core.prompts import ChatPromptTemplate
from langchain_experimental.tools import PythonREPLTool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from src.model_types import SearchProblem,GeneratePython


class CodeGenerationNode:
    def __init__(self, llm):
        self.llm = llm.with_structured_output(GeneratePython)
        
    def run(self, problem:SearchProblem, data: str) -> GeneratePython:
        prompt = ChatPromptTemplate.from_messages([
            ("system",
            "あなたは優秀なPythonエンジニアです。あなたの業務は、正確なPythonコードを生成することです。"),
            ("human",
             """
            以下のデータに対して、以下の問題を解決するようなPythonコードを生成してください。
            データ:{data}
            問題:{problem}

            有効なPythonコードを生成してください。
            内容を書き換えてはいけません。
            出力はcsvファイルとなるようにしてください。不要な改行をしないようにしてください。
            重要：REPLで実行されるため、最後に必ず print(result.rstrip('\n'))文を使って結果を表示してください。
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
            "data": data,
            "problem": problem
        })
                
        return  generated_code












# 確認用
def main():
    load_dotenv()
   
    llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
    code_generator = CodeGenerationNode(llm)
    
    # サンプルデータ
    sample_data =   """
                        id,name,age,city
                        1,田中太郎,28,東京
                        2,佐藤花子,35,大阪
                        3,鈴木一郎,42,名古屋
                        4,山田次郎,31,福岡
                        5,高橋三郎,47,札幌
                    """
    
    # データの説明
    data_description = DataAnalysisResult(data_summary="データ",data_content="これは顧客情報のCSVデータで、ID、名前、年齢、都市の情報が含まれています。")
    
    # コード生成と実行
    result = code_generator.run(
        description=data_description,
        data=sample_data
    )
    
    # 結果の表示
    print("【生成されたコード】")
    print(result.code)
    print("\n【実行結果】")
    print(result.output)

if __name__ == "__main__":
    main()
from langchain_core.prompts import ChatPromptTemplate
from langchain_experimental.tools import PythonREPLTool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from src.model_types import DataAnalysisResult, GeneratedCode

class CodeGenerationNode:
    def __init__(self, llm):
        self.llm = llm
        self.python_repl = PythonREPLTool()
        
    def run(self, description: DataAnalysisResult, data: str) -> GeneratedCode:
        prompt = ChatPromptTemplate.from_messages([
            ("system",
            "あなたは優秀なPythonエンジニアです。あなたの業務は、正確なPythonコードを生成することです。"),
            ("human",
            "以下のデータの最初の3行を取得できるようなPythonコードを生成してください。\n\n"
            "データ:\n{data}\n\n"
            "データに関する説明を添付するので参考にしてください:\n{description}\n\n"
            "内容を書き換えてはいけません。\n\n"
            "出力はcsvファイルとなるようにしてください。不要な改行をしないようにしてください。\n\n"
            "重要：REPLで実行されるため、最後に必ず print() 文を使って結果を表示してください。\n\n"
            "例：\n"
            "```python\n"
            "result = df.head(3).to_csv(index=False)\n"
            "print(result)  # これで結果が表示されます\n"
            "```")
        ])
        
        # まずLLMを使ってコードを生成するチェーンを作成
        chain = prompt | self.llm.with_structured_output(GeneratedCode)
        
        # コードの生成
        generated_code = chain.invoke({
            "data": data,
            "description": description.data_content
        })
        
        # 生成されたコードをPythonREPLで実行
        if generated_code and generated_code.code:
            try:
                execution_result = self.python_repl.invoke(generated_code.code)
                generated_code.output = execution_result
                print(execution_result)
            except Exception as e:
                generated_code.output = f"コード実行エラー: {str(e)}"
                
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
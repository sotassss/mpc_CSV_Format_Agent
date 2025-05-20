from langchain_core.prompts import ChatPromptTemplate
from langchain_experimental.tools import PythonREPLTool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from src.model_types import GeneratePython,ExecutePython


class ExecutionNode:
    def __init__(self, code:GeneratePython):
        self.python_repl = PythonREPLTool()
        self.code=code
       
    def run(self, code:GeneratePython) -> ExecutePython:
        # 生成されたコードをPythonREPLで実行
        if code :
            try:
                execution_result = self.python_repl.invoke(code)
                print(execution_result)
            except Exception as e:
                execution_result = f"コード実行エラー: {str(e)}"
                
        return  execution_result












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
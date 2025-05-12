from langchain_core.prompts import ChatPromptTemplate

from src.model_types import DataAnalysisResult ,GeneratedCode

class CodeGenerationNode:
    def __init__(self,llm):
        self.llm=llm.with_structured_output(GeneratedCode)

    def run(self, description: DataAnalysisResult, data: str) -> GeneratedCode:
        prompt = ChatPromptTemplate.from_messages([
            ("system",
            "あなたは優秀なPythonエンジニアです。あなたの業務は、正確なPythonコードを生成することです。"),
            ("human",
            "以下のデータの最初の3行を取得できるようなPythonコードのみを生成してください。\n\n"
            "データ:\n{data}\n\n"
            "データに関する説明を添付するので参考にしてください:\n{description}\n\n"
            "出力はcsvファイルとなるようにしてください。")
        ])

        chain = prompt | self.llm
        return chain.invoke({
            "data": data,
            "description": description.data_content
        })

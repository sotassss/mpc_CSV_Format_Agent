from langchain_experimental.tools import PythonREPLTool
from src.model_types import GeneratePython, ExecutePython


class CodeExecutionNode:
    """
    Pythonコードを実行する

    Parameters
    ----------
    code : GeneratePython
        実行するPythonコード
    
    Returns
    ----------
    save_path : str
        実行結果を格納したファイルのパス
    """
    def __init__(self):
        self.python_repl = PythonREPLTool()

    def run(self, code: GeneratePython, save_path:str) -> ExecutePython:
        try:
            execution_result = self.python_repl.invoke(code.code)
        except Exception as e:
            execution_result = f"コード実行エラー: {str(e)}"
        
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(execution_result)

        return ExecutePython(output=execution_result)

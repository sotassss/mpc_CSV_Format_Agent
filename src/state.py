from pydantic import BaseModel,Field

from src.model_types import SearchProblem,GeneratePython,ExecutePython,EvaluationData

#グラフのステート定義
class State(BaseModel):
    data_path:str=Field(..., description="元データのパス")
    data_content:str=Field(..., description="元データの内容")
    iteration:int=Field(1, description="試行回数")
    data_problem:SearchProblem =Field(..., description="データの問題点")
    generated_code:GeneratePython = Field(..., description="生成されたPythonコード")
    executed_data:ExecutePython = Field(..., description="成形後のデータ")
    evaluation_result:EvaluationData=Field(..., description="評価結果")
    

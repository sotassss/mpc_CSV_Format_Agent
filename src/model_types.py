from pydantic import BaseModel,Field
from typing import Optional

class SearchProblem(BaseModel):
    problem_list:str = Field(..., description="Tidyデータに変換する際の問題点")

class GeneratePython(BaseModel):
    code: str = Field(description="生成されたPythonコード")

class ExecutePython(BaseModel):
    output: str = Field(description="実行結果")   

class EvaluationData(BaseModel):
    result:bool=Field(..., description="判定結果")
    feedback:str=Field(..., description="フィードバック")
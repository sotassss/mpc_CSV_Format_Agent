from pydantic import BaseModel,Field

class DataAnalysisResult(BaseModel):
    data_summary:str = Field(..., description="データの要約")
    data_content: str = Field(..., description="データの内容")

class GeneratedCode(BaseModel):
    code: str = Field(..., description="生成されたPythonコード")

class ExecutedResult(BaseModel):
    result: str = Field(..., description="実行結果")
    error: str = Field(..., description="エラー内容")

class EvaluationResult(BaseModel):
    result:bool=Field(..., description="判定結果")
    feedback:str=Field(..., description="フィードバック")
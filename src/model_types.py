from pydantic import BaseModel,Field
from typing import Optional

class DataAnalysisResult(BaseModel):
    data_summary:str = Field(..., description="データの要約")
    data_content:str = Field(..., description="データの内容")

class GeneratedCode(BaseModel):
    code: str = Field(description="生成されたPythonコード")
    output: Optional[str] = Field(None, description="コード実行の出力結果")

class EvaluationResult(BaseModel):
    result:bool=Field(..., description="判定結果")
    feedback:str=Field(..., description="フィードバック")
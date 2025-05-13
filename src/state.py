from pydantic import BaseModel,Field

from src.model_types import DataAnalysisResult,GeneratedCode,EvaluationResult

#グラフのステート定義
class State(BaseModel):
    data:str=Field(..., description="元データのパス")
    iteration:int=Field(1, description="試行回数")
    data_analysis_result:DataAnalysisResult=Field(..., description="データ分析結果")
    generated_code:GeneratedCode=Field(..., description="生成されたPythonコード")
    evaluation_result:EvaluationResult=Field(..., description="評価結果")
    

from pydantic import BaseModel,Field

from src.model_types import DataAnalysisResult,GeneratedCode,ExecutedResult,EvaluationResult

#グラフのステート定義
class State(BaseModel):
    data:str=Field(..., description="元データ")
    data_analysis_result:DataAnalysisResult=Field(..., description="データ分析結果")
    generated_code:GeneratedCode=Field(..., description="生成されたPythonコード")
    executed_result:ExecutedResult=Field(..., description="実行結果")
    evaluation_result:EvaluationResult=Field(..., description="評価結果")
    

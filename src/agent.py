from langgraph.graph import END,StateGraph

from src.state import State
from src.model_types import ExecutedResult
from src.utils.proxy import handle_proxy_request

from src.nodes.data_analysis import DataAnalysisNode
from src.nodes.code_execution import CodeExecutionNode
from src.nodes.code_generation import CodeGenerationNode
from src.model_types import DataAnalysisResult,GeneratedCode,ExecutedResult,EvaluationResult

class ExcelFormat:
    def __init__(self,llm):
        self.data_analysis_node = DataAnalysisNode(llm)
        self.code_generation_node = CodeGenerationNode(llm)
        self.code_execution_node = CodeExecutionNode(llm)

        #グラフ作成
        self.graph=self._create_graph()

    def _create_graph(self)->StateGraph:
        # 初期化
        workflow=StateGraph(State)

        #ノードの追加
        workflow.add_node("data_analysis",self._analyze_data)
        workflow.add_node("code_generation",self._code_generation)
        # workflow.add_node("code_execution",self._code_execution)
        
        # 開始点の追加
        workflow.set_entry_point("data_analysis")

        # ノード間の接続
        workflow.add_edge("data_analysis","code_generation")
        # workflow.add_edge("code_generation","code_execution")

        return workflow.compile()
    

    def run(self,data:str)->ExecutedResult:
        # ステートの初期化
        initial_state = State(
            data=data,
            data_analysis_result=DataAnalysisResult(data_summary="概要",data_content=data),  # 初期のデータ分析結果
            generated_code=GeneratedCode(code="生成されたPythonコード"),  # 初期の生成コード
            executed_result=ExecutedResult(result="実行成功", error=""),  # 初期の実行結果
            evaluation_result=EvaluationResult(result=True, feedback="問題なし")  # 初期の評価結果
        )

        # ワークフローの実行
        result=self.graph.invoke(initial_state)

        # 結果を返す
        return result['generated_code'].output # 実行結果を返す
        


    # 各ノードにおける処理
    def _analyze_data(self,state:State):
        handle_proxy_request()  # プロキシ設定を自動で切り替える処理
        print("データ分析中...")
        data_analysis_result=self.data_analysis_node.run(data=state.data)
        return {"data_analysis_result":data_analysis_result}
    
    def _code_generation(self,state:State):
        handle_proxy_request()  # プロキシ設定を自動で切り替える処理
        print("Pythonコード生成中...")
        code_generation=self.code_generation_node.run(
            description=state.data_analysis_result,
            data=state.data
        )
        return {"generated_code":code_generation}
    
    def _code_execution(self,state:State):
        handle_proxy_request()  # プロキシ設定を自動で切り替える処理
        print("Pythonコード実行中...")
        code_execution_result=self.code_execution_node.run(
            data=state.data_analysis_result,
            generated_code=state.generated_code,
        )
        return {"executed_result":code_execution_result}
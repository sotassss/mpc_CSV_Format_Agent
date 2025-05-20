from langgraph.graph import END,StateGraph

from src.state import State
from src.utils.proxy import handle_proxy_request

from nodes.search_problem_node import SearchProblemNode
from nodes.code_generation_node import CodeGenerationNode
from nodes.code_execution_node import CodeExecutionNode
from nodes.result_evaluation_node import ResultEvaluationNode
from src.model_types import SearchProblem,GeneratePython,ExecutePython,EvaluationData


class ExcelFormat:
    def __init__(self,llm,maximum_iteration:int=3):
        self.maximum_iteration=maximum_iteration
        self.search_problem_node = SearchProblemNode(llm)
        self.code_generation_node = CodeGenerationNode(llm)
        self.code_execution_node = CodeExecutionNode()
        self.evaluation_node = ResultEvaluationNode(llm)

        #グラフ作成
        self.graph=self._create_graph()

    def _create_graph(self)->StateGraph:
        # 初期化
        workflow=StateGraph(State)

        #ノードの追加
        workflow.add_node("search_problem",self._search_problem)
        workflow.add_node("code_generation",self._code_generation)
        workflow.add_node("code_execution",self._code_execution)
        workflow.add_node("result_evaluation",self._result_evaluation)
        
        # 開始点の追加
        workflow.set_entry_point("search_problem")

        # ノード間の接続
        workflow.add_edge("data_analysis","code_generation")
        workflow.add_edge("code_generation","code_execution")
        workflow.add_edge("code_execution","result_evaluation")

        workflow.add_conditional_edges(
            "result_evaluation",
            lambda state: not state.evaluation_result.result and state.iteration <= self.maximum_iteration,
            {True:"search_problem", False:END}
            )

        return workflow.compile()
    

    def run(self,data_path:str)->GeneratePython:
        # ステートの初期化
        initial_state = State(
            data_path=data_path,
            iteration=1,
            data_problem=SearchProblem(problem="問題"),  # 初期のデータ分析結果
            generated_code=GeneratePython(code="生成されたPythonコード"),  # 初期の生成コード
            executed_data=ExecutePython(result="実行結果"),  # 初期の実行結果
            evaluation_result=EvaluationData(result=True, feedback="問題なし")  # 初期の評価結果
        )

        # ワークフローの実行
        result=self.graph.invoke(initial_state)

        # 結果を返す
        return result 
        


    # 各ノードにおける処理
    def _search_problem(self,state:State):
        handle_proxy_request()  # プロキシ設定を自動で切り替える処理
        print("問題探索中...")
        data_analysis_result=self.data_analysis_node.run(data=state.data)
        return {"data_analysis_result":data_analysis_result}
    
    def _code_generation(self,state:State):
        handle_proxy_request()  # プロキシ設定を自動で切り替える処理
        if state.iteration<=1:
            print("Pythonコード生成中...")
        else:
            print(f"再度Pythonコード生成中...{state.iteration}/{self.maximum_iteration}回目")
        code_generation=self.code_generation_node.run(
            problem=state.data_problem,
            data=state.data
        )
        return {"generated_code":code_generation}
    
    def _code_execution(self,state:State):
        handle_proxy_request()  # プロキシ設定を自動で切り替える処理
        print("Pythonコード実行中...")
        code_execution_result=self.code_execution_node.run(
            code=state.generated_code
        )
        return {"executed_result":code_execution_result}
    
    def _result_evaluation(self,state:State):
        print("結果を評価しています...")
        evaluation_result=self.result_evaluation_node.run(
            execution_result=state.executed_data)
        return {"evaluation_result":evaluation_result,
                "iteration":state.iteration+1}
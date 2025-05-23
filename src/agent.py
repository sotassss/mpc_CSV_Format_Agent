import pandas as pd
from langgraph.graph import END,StateGraph

from src.state import State
from src.utils.proxy import handle_proxy_request

from src.nodes.search_problem_node import SearchProblemNode
from src.nodes.code_generation_node import CodeGenerationNode
from src.nodes.code_execution_node import CodeExecutionNode
from src.nodes.result_evaluation_node import ResultEvaluationNode
from src.model_types import SearchProblem,GeneratePython,ExecutePython,EvaluationData


class ExcelFormat:
    def __init__(self,llm,maximum_iteration:int=3):
        self.maximum_iteration=maximum_iteration
        self.search_problem_node = SearchProblemNode(llm)
        self.code_generation_node = CodeGenerationNode(llm)
        self.code_execution_node = CodeExecutionNode()
        self.result_evaluation_node = ResultEvaluationNode(llm)

        self.graph=self._create_graph()

    def _create_graph(self)->StateGraph:
        workflow=StateGraph(State)

        workflow.add_node("search_problem",self._search_problem)
        workflow.add_node("code_generation",self._code_generation)
        workflow.add_node("code_execution",self._code_execution)
        workflow.add_node("result_evaluation",self._result_evaluation)
        
        workflow.set_entry_point("search_problem")

        workflow.add_edge("search_problem","code_generation")
        workflow.add_edge("code_generation","code_execution")
        workflow.add_edge("code_execution","result_evaluation")

        workflow.add_conditional_edges(
            "result_evaluation",
            lambda state: not state.evaluation_result.result and state.iteration <= self.maximum_iteration,
            {True:"search_problem", False:END}
            )

        return workflow.compile()
    

    def run(self,data_path:str)->str:
        # 初期化
        initial_state = State(
                data_path=data_path,
                data_content="",
                iteration=1,
                data_problem=SearchProblem(problem="抽出された問題"),  
                generated_code=GeneratePython(code="生成されたPythonコード"),
                executed_data=ExecutePython(output="成形後のデータ"),  
                evaluation_result=EvaluationData(result=True, feedback="フィードバック結果")
            )

        # ワークフローの実行
        final_state=self.graph.invoke(initial_state)

        return final_state["data_path"]
        

    # 各ノードにおける処理
    def _search_problem(self,state:State):
        handle_proxy_request()  # プロキシ処理
        data_df = pd.read_csv(state.data_path, encoding="utf-8")
        data_content = data_df.to_csv(index=False, encoding="utf-8")
        print("問題探索中...")
        data_problem = self.search_problem_node.run(
            data_path=state.data_path,
            data_content=data_content
            )
        return {
            "data_content": data_content,
            "data_problem": data_problem
            }
    
    def _code_generation(self,state:State):
        handle_proxy_request()  # プロキシ処理

        if state.iteration<=1:
            print("Pythonコード生成中...")
        else:
            print(f"再度Pythonコード生成中...{state.iteration}/{self.maximum_iteration}回目")

        data_df = pd.read_csv(state.data_path, encoding="utf-8")
        data_content = data_df.to_csv(index=False, encoding="utf-8")
        generated_code = self.code_generation_node.run(
            data_path=state.data_path,
            data_content=data_content,
            problem=state.data_problem
        )
        return {
            "generated_code": generated_code,
            "data_content": data_content
            }
    
    def _code_execution(self,state:State):
        handle_proxy_request()  # プロキシ処理
        print("Pythonコード実行中...")
        executed_data = self.code_execution_node.run(
            code=state.generated_code
            )
        return {
            "executed_data": executed_data
            }
    
    def _result_evaluation(self,state:State):
        data_df = pd.read_csv(state.data_path, encoding="utf-8")
        execution = data_df.to_csv(index=False, encoding="utf-8")
        handle_proxy_request()  # プロキシ処理
        print("結果を評価しています...")
        evaluation_result = self.result_evaluation_node.run(
            execution
            )
        return {
            "evaluation_result": evaluation_result,
            "iteration": state.iteration+1
            }
## CSV Format Agent

### 各ノード
#### **SearchProblem Node** 
- **目的：** 入力データの構造上の問題点（例：欠損値、整形不備、形式のばらつきなど）を特定する。  
- **入力：** CSVファイルのパス
- **出力：** 問題点

#### **GeneratePython Node**
- **目的：** 検出された問題に基づき、それを解決するためのPythonコードを生成する。
- **入力：** 問題点
- **出力：** Pythonコード

#### **ExecutePython Node**
- **目的：** 生成されたPythonコードを実行し、CSVデータを整形する。
- **入力：** Pythonコード
- **出力：** 実行結果

#### **EvaluationResult Node**
- **目的：** 整形後のデータに問題が残っていないかを評価し、改善が必要な場合には再度ループを回す。
- **入力：** 実行結果
- **出力：** 評価結果

### ステート図
<img width="350" alt="IRエージェント　ステート図 (1)" src="https://github.com/user-attachments/assets/fe70c47e-748a-48b3-ba2f-4a58bb266a51" />

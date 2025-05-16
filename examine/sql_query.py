from langchain import LLMChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import sqlite3
import pandas as pd
import os

try:
    # 1. データベースの存在確認
    db_path = "my_data.db"
    
    # 2. まずDBのテーブル構造を調べる
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # データベース内のテーブル一覧を取得
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("データベース内のテーブル:", [table[0] for table in tables])
    
    table_info = {}
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        table_info[table_name] = columns
        print(f"\nテーブル '{table_name}' の構造:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
    
    # 3. LLMインスタンス生成
    try:
        llm = ChatOpenAI(model="gpt-4.1-nano")
    except Exception as e:
        print(f"OpenAI APIエラー: {e}")
        print("モデル名が正しいか、APIキーが設定されているか確認してください。")
        print("代替として別のモデルを試します。")
        llm = ChatOpenAI(model="gpt-3.5-turbo")  # フォールバックとして別のモデルを試す
    
    # 4. テーブル情報を含めたプロンプトの設定
    tables_info_str = "\n".join([f"テーブル名: {table_name}\nカラム: {', '.join([col[1] for col in cols])}" 
                               for table_name, cols in table_info.items()])
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"あなたはSQLを生成するアシスタントです。以下のデータベース構造を参考にしてください。\n{tables_info_str}"),
        ("user", "検索条件: {condition} に合うSQLite用のSQLを書いてください。SQLクエリのみを返してください。")
    ])
    
    # 5. LLMChainの生成
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # 6. 自然言語条件
    user_input = """
    表構造が複数含まれています。
    この中で、「重要指数」の表構造を解析し、行の項目名を出力してください。
    大項目・中項目を含むような場合は、最も小さい分類まで表示してください。
    大項目を例示すると、「獲得数計」や「wel-fit」などのような分類のことです。
    """
    
    # 7. SQL生成
    print(f"\n入力: {user_input}")
    sql_query = chain.run(condition=user_input)
    print("\n生成されたSQLクエリ:\n", sql_query.strip())
    
    # 8. SQLiteでクエリ実行
    df_result = pd.read_sql(sql_query, conn)
    print("\n実行結果:")
    print(df_result)
        
    conn.close()

except Exception as e:
    print(f"全体エラー: {e}")
    print("エラーの詳細情報:", e.__class__.__name__)
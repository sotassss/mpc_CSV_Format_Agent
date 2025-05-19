import os
import pandas as pd
excel = pd.ExcelFile("C:/Users/1109685/Documents/IR/Sample_freejob_short.xlsx")
dataframe_data = pd.read_excel(excel, sheet_name=0)

json_data = dataframe_data.to_json(orient="records", force_ascii=False)
# markdown_data = dataframe_data.to_markdown()

# os.makedirs("output", exist_ok=True)
# with open("output/data_output.json", "w", encoding="utf-8") as f:
#     f.write(json_data)

with open("output/data_output_color_short_modified.md", "r", encoding="utf-8") as f:
    markdown_data = f.read()

with open("output/data_output_color_short.html", "r", encoding="utf-8") as f:
    html_data = f.read()


# 生成AI系のインポート
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4.1-nano")
prompt = ChatPromptTemplate.from_messages([
    ("system", "あなたは優秀なデータ分析者です。"),
    ("human", """
                以下のデータを分析してください。
                データの内容は{data}です。
                「◆重要指数」の表構造を解析し、行の項目名を出力してください
                階層構造の読解において、色の情報を参考にしてください。
                階層構造を正しく理解してください。
                余計な情報は含まず、重複に注意してください。
                大項目・中項目を含むような場合は、最も小さい項目まで表示してください。
                大項目を例示すると、「獲得数計」や「wel-fit」などのような分類のことです。
                中項目を例示すると、「レギュラー」や「アドバンス」のような分類のことです。
                回答は以下の形式ですべての項目を答えてください。
                重複しないようにしてください。

                ◆重要指数：
                大項目1:
                    - 中項目1
                    - 中項目2
                    - 中項目3
                大項目2:
                    - 中項目1
                    .....
                
                回答形式を遵守し、回答のみを表示してください。
            """),
    # ("human","""
    #             以下のデータを分析してください。    
    #             データの内容は{data}です。
    #             不要な列、不要な行を削除するpythonコードを生成してください。
    #             """)
    #             ,
])

chain = prompt | llm

result = chain.invoke({"data": html_data})
# result = chain.invoke({"data": json_data})

print(result.content)

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

with open("output/data_output_color_short_format.html", "r", encoding="utf-8") as f:
    html_data = f.read()


# 生成AI系のインポート
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4.1-nano")
prompt = ChatPromptTemplate.from_messages([
    ("system", "あなたは表構造解析のスペシャリストです。"),
    ("human", """
    まず、以下の表構造を縦方向に解析してください。
    表構造 : {data}
    そして、列の項目名をすべて列挙してください。
     横方向は考えなくてよいです。
     色の情報、枠線の情報を活用してください。
     アルバイトという項目名はありますか。

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

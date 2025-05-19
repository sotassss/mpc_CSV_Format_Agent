import base64
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()


image_path="C:/Users/1109685/Documents/IR/examine/image_llm.py"

with open(image_path, "rb") as image_file:
    encoded_string=base64.b64encode(image_file.read()).decode('utf-8')

llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_messages([
    ("system", "あなたは優秀なデータ分析者です。"),
    ("human", """
                以下のデータを分析してください。
                データの内容は{data}です。
                この表には複数の表構造が含まれています。
                「◆重要指数」の表構造を解析し、行の項目名を出力してください。
                大項目・中項目を含むような場合は、最も小さい分類まで表示してください。
                大項目を例示すると、「獲得数計」や「wel-fit」などのような分類のことです。
                中項目を例示すると、「レギュラー」や「アドバンス」のような分類のことです。
                回答は以下の形式ですべての項目を答えてください。
                必ずデータに含まれた項目名のみで回答を生成してください。

                ◆重要指数：
                大項目1:
                    - 中項目1
                    - 中項目2
                    - 中項目3
                    ......
                大項目2:
                    - 中項目1
                    .....
                
                回答形式を遵守し、回答のみを表示してください。
            """),
])

chain = prompt | llm

# result = chain.invoke({"data": markdown_data})
result = chain.invoke({"data": encoded_string})

print(result.content)




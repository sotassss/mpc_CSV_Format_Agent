# データの読み込み
import os
import pandas as pd 
excel = pd.ExcelFile("C:/Users/1109685/Documents/IR/Sample_freejob.xlsx")
dataframe_data=pd.read_excel(excel, sheet_name=0)
markdown_data = dataframe_data.to_markdown(index=False)
os.makedirs("output", exist_ok=True)
with open("output/markdown_output.md", "w", encoding="utf-8") as f:
    f.write(markdown_data)
# markdown_data = dataframe_data.head(100).to_markdown(index=False)
# print(markdown_data)



# 生成AI系のインポート
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm=ChatOpenAI(model="gpt-4.1-nano")
prompt = ChatPromptTemplate.from_messages([
    ("system", "あなたは優秀なデータ分析者です。"),
    ("human", """
                以下のデータを分析してください。
                データの内容は{data}です。
                この表には複数の表構造が含まれています。
                「◆重要指数」の表構造を解析し、行タイトルを出力してください。
                大分類・中分類を含むような場合は、最も小さい分類まで表示してください。
                大分類を例示すると、「獲得数計」や「wel-fit」などのような分類のことです。
                中分類を例示すると、「レギュラー」や「アドバンス」のような分類のことです。
                回答は以下の形式で答えてください。
                
                重要指数：
                大分類1:
                    - 中分類1
                        - 小分類1
                        - 小分類2
                    - 中分類2
                    - 中分類3
                        - 小分類1
                        - 小分類2
                大分類2:
                    - 中分類1
                    - 中分類2
                大分類3:
                .....
     

                回答のみを表示してください。
            """),   
])


chain=prompt | llm

result=chain.invoke({"data": markdown_data})
print(result.content)
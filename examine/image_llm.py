import base64
from openai import OpenAI

# OpenAIクライアントの初期化（APIキーを環境変数か直接指定）
client = OpenAI()

# 画像をbase64に変換
image_path = "C:/Users/1109685/Documents/IR/examine/output/image.png"
with open(image_path, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

# メッセージ送信
response = client.chat.completions.create(
    model="gpt-4o-mini",  # 画像対応モデル
    # model="gpt-4.1-nano",  
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": """
                            以下の添付画像は財務管理エクセルのスクリーンショットです。
                            画像内の表構造を分析してください。
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
                            大項目2:
                                - 中項目1
                            """
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{encoded_image}"
                    }
                }
            ]
        }
    ],
    temperature=0.2,
    max_tokens=2000
)

print(response.choices[0].message.content)

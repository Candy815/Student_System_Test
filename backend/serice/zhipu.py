from zhipuai import ZhipuAI
import os
from dotenv import load_dotenv
load_dotenv()

Zhipu_API_Key = os.getenv("Zhipu_API_Key")
client = ZhipuAI(api_key=Zhipu_API_Key)  # 请填写您自己的 API Key

response = client.chat.completions.create(
    model="glm-4.5",
    messages=[
        {"role": "user", "content": "作为一名营销专家，请为我的产品创作一个吸引人的口号"},
        {"role": "assistant", "content": "当然，要创作一个吸引人的口号，请告诉我一些关于您产品的信息"},
        {"role": "user", "content": "智谱AI开放平台"}
    ],
    thinking={
        "type": "enabled",    # 启用深度思考模式
    },
    stream=True,              # 启用流式输出
    max_tokens=4096,          # 最大输出tokens
    temperature=0.6           # 控制输出的随机性
)

# 流式获取回复
for chunk in response:
    if chunk.choices[0].delta.reasoning_content:
        print(chunk.choices[0].delta.reasoning_content, end='', flush=True)

    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end='', flush=True)
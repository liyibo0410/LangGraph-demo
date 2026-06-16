import asyncio
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(
    api_key=os.getenv("SILICON_API_KEY"),
    base_url=os.getenv("SILICON_BASE_URL")
)
MODEL = "deepseek-ai/DeepSeek-V4-Flash"

# 机试3要求：系统 + 人类 + AI 三角色历史对话
messages = [
    {"role": "system", "content": "你是专业BIM工程师，回答专业简洁"},
    {"role": "user", "content": "BIM和CAD的区别是什么？"},
    {"role": "assistant", "content": "BIM是带信息的三维模型，CAD是二维绘图工具。"},
    {"role": "user", "content": "BIM常用软件有哪些？"}
]

# 调用大模型
res = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    temperature=0.6
)

# 输出结果
print("===== 机试3 三角色对话 =====")
for msg in messages:
    role = msg["role"]
    if role == "system": role = "system"
    elif role == "user": role = "human"
    elif role == "assistant": role = "ai"
    print(f"[{role}] {msg['content']}")

answer = res.choices[0].message.content
print(f"\n[AI回复] {answer}")

# TOKEN 统计
print("\n===== TOKEN 统计 =====")
print(f"输入Token：{res.usage.prompt_tokens}")
print(f"输出Token：{res.usage.completion_tokens}")
print(f"总Token：{res.usage.total_tokens}")
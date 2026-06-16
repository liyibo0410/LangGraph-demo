# 必加：加载.env密钥
from dotenv import load_dotenv
load_dotenv()

import os
import asyncio
from langchain_openai import ChatOpenAI

# 正确配置模型（你的硅基流动）
llm = ChatOpenAI(
    model="Qwen/Qwen2.5-7B-Instruct",  # 最稳定免费
    api_key=os.getenv("SILICON_API_KEY"),
    base_url=os.getenv("SILICON_BASE_URL"),
    temperature=0.7
)

# ----------------------
# 1. 同步调用
# ----------------------
print("=== 同步调用 ===")
response = llm.invoke("你好")
print(response.content)

# ----------------------
# 2. 流式调用（逐字输出）
# ----------------------
print("\n=== 流式调用 ===")
for chunk in llm.stream("讲一个很短的故事"):
    print(chunk.content, end="")

# ----------------------
# 3. 批量调用
# ----------------------
print("\n\n=== 批量调用 ===")
responses = llm.batch(["你好", "再见", "谢谢"])
for i, res in enumerate(responses):
    print(f"{i+1}: {res.content}")

# ----------------------
# 4. 异步调用
# ----------------------
print("\n=== 异步调用 ===")
async def async_test():
    res = await llm.ainvoke("你好")
    print(res.content)

asyncio.run(async_test())# 必加：加载.env密钥
from dotenv import load_dotenv
load_dotenv()

import os
import asyncio
from langchain_openai import ChatOpenAI

# 正确配置模型（你的硅基流动）
llm = ChatOpenAI(
    model="Qwen/Qwen2.5-7B-Instruct",  # 最稳定免费
    api_key=os.getenv("SILICON_API_KEY"),
    base_url=os.getenv("SILICON_BASE_URL"),
    temperature=0.7
)

# ----------------------
# 1. 同步调用
# ----------------------
print("=== 同步调用 ===")
response = llm.invoke("你好")
print(response.content)

# ----------------------
# 2. 流式调用（逐字输出）
# ----------------------
print("\n=== 流式调用 ===")
for chunk in llm.stream("讲一个很短的故事"):
    print(chunk.content, end="")

# ----------------------
# 3. 批量调用
# ----------------------
print("\n\n=== 批量调用 ===")
responses = llm.batch(["你好", "再见", "谢谢"])
for i, res in enumerate(responses):
    print(f"{i+1}: {res.content}")

# ----------------------
# 4. 异步调用
# ----------------------
print("\n=== 异步调用 ===")
async def async_test():
    res = await llm.ainvoke("你好")
    print(res.content)

asyncio.run(async_test())
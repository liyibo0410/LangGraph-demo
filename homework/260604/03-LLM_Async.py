# import asyncio
# from  langchain_openai import ChatOpenAI
#
# llm = ChatOpenAI(model="deepseek-ai/DeepSeek-V4-Flash")
#
# async def call_llm_async():
#     res = await llm.ainvoke("什么是快乐星球?")
#     print(res.content)
#
# asyncio.run(call_llm_async())
import time
import asyncio
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="deepseek-ai/DeepSeek-V4-Flash")

# 准备 5 个测试问题
prompts = [
    "用一句话介绍一下北京",
    "用一句话介绍一下上海",
    "用一句话介绍一下广州",
    "用一句话介绍一下深圳",
    "用一句话介绍一下杭州"
]


# ========== 测试一：同步 invoke（串行） ==========
def test_sync_invoke():
    print("=== 同步 invoke ===")
    start_time = time.time()

    for i, prompt in enumerate(prompts):
        print(f"  [同步] 正在发送第 {i + 1} 个请求...")
        llm.invoke(prompt)  # 死等，拿到结果才进入下一次循环

    print(f"总耗时: {time.time() - start_time:.2f} 秒\n")


# ========== 测试二：异步 ainvoke（并行） ==========
async def test_async_ainvoke():
    print("=== 异步 ainvoke ===")
    start_time = time.time()

    # 关键：用 asyncio.gather 同时派发所有请求
    print("  [异步] 瞬间派发 5 个请求...")
    tasks = [llm.ainvoke(prompt) for prompt in prompts]
    results = await asyncio.gather(*tasks)

    for r in results:
        print(f"  回答: {r.content[:20]}...")

    print(f"总耗时: {time.time() - start_time:.2f} 秒\n")


# ========== 运行对比 ==========
async def main():
    test_sync_invoke()         # 先跑同步
    await test_async_ainvoke() # 再跑异步

asyncio.run(main())
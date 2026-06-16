import time
import asyncio
from langchain_openai import ChatOpenAI
#
llm = ChatOpenAI(model="deepseek-ai/DeepSeek-V4-Pro",temperature=1)
# print("AI..回答")
# full_msg = None # 存大模型给我们返回的消息
# for chunk in llm.stream("请写一个关于爱情的长诗"):
#     full_msg = chunk if full_msg is None else full_msg + chunk
#     print(chunk.content,end="",flush=True)
#     time.sleep(0.01)
#
# print("---------------------------------------------")
# print(f"\n\n完整消息:\n{full_msg.content}")


async def stream_events():
    async for event in llm.astream_events("你好"):
        if event["event"] == "on_chat_model_start":
            print("开始对话")
        elif event["event"] == "on_chat_model_stream":
            print("对话中")
        elif event["event"] == "on_chat_model_end":
            print("完成")
asyncio.run(stream_events())
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("SILICON_API_KEY"),base_url=os.getenv("SILICON_BASE_URL"))
MODEL = "deepseek-ai/DeepSeek-V4-Flash"

async def BIM_chat():
    # ========= 老师的写法：先定义三个消息变量 =========
    usermassage = "请问BIM解决碰撞的核心举措有哪些？"
    systemmassage = "你是一名BIM建筑师，回答精简通俗，擅长BIM知识讲解"
    AImassage = "优化标高，优化构件位置，优化构件路线"
    next_user = "那BIM有什么其他应用？"

    # 再组装成对话列表
    BIM_msg = [
        {"role":"system","content": systemmassage},
        {"role":"user","content": usermassage},
        {"role":"assistant","content": AImassage},
        {"role":"user","content": next_user}
    ]

    resp = await client.chat.completions.create(model=MODEL,messages=BIM_msg,stream=False,temperature=0.2)
    print("=====完整历史对话记录=====")
    for msg in BIM_msg:
        print(f"[{msg['role']}]：{msg['content']}")
    print(f"\n[AI新回复]：{resp.choices[0].message.content}")
    print("\n=====TOKEN消耗=====")
    print(f"输入Token：{resp.usage.prompt_tokens} | 输出Token：{resp.usage.completion_tokens} | 总计：{resp.usage.total_tokens}")

if __name__ == "__main__":
    asyncio.run(BIM_chat())
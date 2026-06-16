import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("SILICON_API_KEY"),base_url=os.getenv("SILICON_BASE_URL"))
MODEL = "deepseek-ai/DeepSeek-V4-Flash"

question_list = [
    "1*2=？",
    "1*3=？",
    "1*4=？"
]

async def single_query(question):
    res = await client.chat.completions.create(
        model=MODEL,
        messages=[{"role":"user","content":question}],
        stream=False,
        temperature=0.2
    )
    return res

async def batch_ask():
    total_prompt = total_comp = total_all = 0
    print("=====批量问答结果=====\n")
    for idx, q in enumerate(question_list):
        res = await single_query(q)
        print(f"【问题{idx+1}】{q}")
        print(f"回答：{res.choices[0].message.content}\n")
        total_prompt += res.usage.prompt_tokens
        total_comp += res.usage.completion_tokens
        total_all += res.usage.total_tokens
    print("=====批量汇总TOKEN=====")
    print(f"总输入Token：{total_prompt} | 总输出Token：{total_comp} | 总消耗Token：{total_all}")

if __name__ == "__main__":
    asyncio.run(batch_ask())
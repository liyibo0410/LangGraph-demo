import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = AsyncOpenAI(
    api_key=os.getenv("SILICON_API_KEY"),
    base_url=os.getenv("SILICON_BASE_URL")
)
# 截图指定可用模型
MODEL = "deepseek-ai/DeepSeek-V4-Flash"

async def generate_song():
    # 非流式异步调用，满足题目约束
    resp = await client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": "创作一首古风歌曲，包含歌名、主歌、副歌，主题是山河秋景"}],
        stream=False,
        temperature=0.2
    )
    print("=====AI生成古风歌曲=====\n", resp.choices[0].message.content)
    print("\n=====TOKEN消耗统计=====")
    print(f"输入Prompt Token：{resp.usage.prompt_tokens}")
    print(f"输出Completion Token：{resp.usage.completion_tokens}")
    print(f"合计总Token：{resp.usage.total_tokens}")

if __name__ == "__main__":
    asyncio.run(generate_song())
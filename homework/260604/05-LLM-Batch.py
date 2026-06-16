import time
import asyncio
from langchain_openai import ChatOpenAI
#
llm = ChatOpenAI(model="deepseek-ai/DeepSeek-V4-Pro",temperature=1)

questions = [
    "什么是Python？",
    "什么是JavaScript？",
    "什么是Go语言？"
]

responses = llm.batch(questions)
for q, r in zip(questions, responses):
    print(f"Q: {q}")
    print(f"A: {r.content}\n")
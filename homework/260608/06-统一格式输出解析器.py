# 必加：加载.env环境变量
from dotenv import load_dotenv
load_dotenv()

import os
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

# 1. 初始化LLM（你写的完美配置）
llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V4-Flash",
    temperature=0,
    base_url=os.getenv("SILICON_BASE_URL"),
    api_key=os.getenv("SILICON_API_KEY")
)

# 2. 定义Pydantic结构化输出格式
class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

# 3. 绑定结构化输出
structured_llm = llm.with_structured_output(schema=CalendarEvent)

# 4. 调用（自动提取信息 → 塞进结构体）
result = structured_llm.invoke("Alice and Bob are going to a science fair on Friday.")

# 输出结果
print(result)
print(type(result))  # <class '__main__.CalendarEvent'>
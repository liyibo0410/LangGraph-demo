# 必加：加载环境变量
from dotenv import load_dotenv
load_dotenv()

import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field

# 提示词
prompt = ChatPromptTemplate.from_template("请用{xxx}风格回答：{question}")

llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V4-Flash",
    temperature=0,
    base_url=os.getenv("SILICON_BASE_URL"),
    api_key=os.getenv("SILICON_API_KEY")
)

# 定义结构化输出格式
class Demo(BaseModel):
    title: str = Field(description='用户原始的问题')
    content: str = Field(description="大模型对于用户原始问题的回答")

# 绑定结构化输出
llm_with_demo = llm.with_structured_output(schema=Demo)

# LCEL 链
chain = prompt | llm_with_demo

# 执行
res = chain.invoke({
    "xxx": '幽默',
    "question": '什么是爱?'
})

# 输出结果
print(type(res))       # <class '__main__.Demo'>
print(res.title)       # 什么是爱?
print(res.content)     # 幽默风格的回答
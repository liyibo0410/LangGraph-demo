# 必加：加载环境变量
from dotenv import load_dotenv
load_dotenv()

import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 大模型对象（你写的完美配置 ✅）
llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V4-Flash",
    temperature=0,
    base_url=os.getenv("SILICON_BASE_URL"),
    api_key=os.getenv("SILICON_API_KEY")
)

# 提示词
prompt = ChatPromptTemplate.from_template(
    '你是一个资深的宠物起名大师,请为一只{color}颜色的{breed}起3个搞笑的名字'
)

# 链式调用
chain = prompt | llm | StrOutputParser()

# 执行
res = chain.invoke({
    'color': '橘色',
    'breed': '狸花猫'
})

# 输出
print(res)
print(type(res))  # 一定是 <class 'str'>
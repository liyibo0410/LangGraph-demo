# 必加：加载环境变量
from dotenv import load_dotenv
load_dotenv()

import os
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# 模型配置（你写的非常标准 ✅）
llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V4-Flash",
    temperature=0.0,
    base_url=os.getenv("SILICON_BASE_URL"),
    api_key=os.getenv("SILICON_API_KEY")
)

# 定义结构化输出格式
class Demo(BaseModel):
    name: str = Field(description="收件人姓名")
    phone: str = Field(description='收件手机号')
    address: str = Field(description='收件人地址')

# 绑定结构化输出
sp = llm.with_structured_output(schema=Demo)

# 快递信息
raw_text = "给张三寄个快递，电话是13812345678。地址在上海市浦东新区世纪大道1号金茂大厦5楼。"

# 调用
res = sp.invoke(raw_text)

# 输出
print(res)
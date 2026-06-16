# 必加：加载环境变量
from dotenv import load_dotenv
load_dotenv()

import os
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

# 大模型配置（你写的标准写法 ✅）
llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V4-Flash",
    temperature=0,
    base_url=os.getenv("SILICON_BASE_URL"),
    api_key=os.getenv("SILICON_API_KEY")
)

# 1. 定义输出格式
class Prime(BaseModel):
    prime: list[int] = Field(description="素数列表")
    count: list[int] = Field(description="每个素数对应的小于它的素数个数")

# 2. 创建 JSON 解析器
json_parser = JsonOutputParser(pydantic_object=Prime)

# 3. 打印格式要求（大模型必须按这个格式输出）
print("===== 格式要求 =====")
print(json_parser.get_format_instructions())
print("="*50)

# 4. 拼接提示词 + 调用模型
res = llm.invoke([
    ("system", json_parser.get_format_instructions()),
    ("user", "任意生成5个1000-100000之间的素数，并标出小于该素数的素数个数")
])

# 5. 查看原始返回
print("\n===== 模型原始输出 =====")
print(res.content)

# 6. 解析成字典
parsed_res = json_parser.invoke(res)
print("\n===== 解析后结果 =====")
print(parsed_res)
print("类型：", type(parsed_res))  # <class 'dict'>
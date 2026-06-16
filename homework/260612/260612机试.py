from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
# 提示词、管道、输出解析器
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
load_dotenv()

llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V4-Flash",
    temperature=0.0,
    base_url=os.getenv("SILICON_BASE_URL"),
    api_key=os.getenv("SILICON_API_KEY")
)

class UserInfo(BaseModel):
    name: str = Field(description="收件人的姓名")
    phone: str = Field(description="收件人的联系手机号码")
    address: str = Field(description="完整的收货地址")

structured_llm = llm.with_structured_output(UserInfo).with_retry(stop_after_attempt=3)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是专业的电商客服，根据用户提供的收件人姓名、手机号、收货地址，生成一段亲切礼貌的发货确认回复。"),
        ("human", "收件人姓名：{name}，手机号：{phone}，收货地址：{address}")
    ]
)
output_parser = StrOutputParser()

# 核心修正：新增 Pydantic 转字典的步骤，适配提示词模板的输入要求
chain = (
    structured_llm
    | RunnableLambda(lambda user_info: user_info.model_dump())
    | prompt
    | llm
    | output_parser
).with_retry(stop_after_attempt=3)

def run_task(user_text: str):
    user_info = structured_llm.invoke(user_text)

    print("=== 1. 成功提取结构化数据 ===")
    print(f"收件人: {user_info.name}")
    print(f"手机号: {user_info.phone}")
    print(f"收货地址: {user_info.address}")

    reply = chain.invoke(user_text)
    print("\n=== 2. 自动生成客服回复 ===")
    print(reply)
    print("-" * 50 + "\n")

if __name__ == "__main__":
    # 案例1
    print("===== 案例1 =====")
    text_a = "给张三发个件，电话是13812345678。地址在上海市浦东新区世纪大道1号金茂大厦5楼。"
    run_task(text_a)

    # 案例2
    print("===== 案例2 =====")
    text_b = "顺丰送去北京朝阳区建国门外大街1号国贸大厦吧，找李四拿，顺便说下他电话是13998765432。"
    run_task(text_b)
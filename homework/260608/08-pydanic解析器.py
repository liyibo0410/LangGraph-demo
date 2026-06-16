# 必加：加载.env环境变量
from dotenv import load_dotenv
load_dotenv()

import os
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

# 1. 定义数据模型（保持不变）
class MovieReview(BaseModel):
    """电影评论结构"""
    title: str = Field(description="电影标题")
    rating: int = Field(description="评分，1-10分", ge=1, le=10)
    summary: str = Field(description="剧情简介")
    recommended: bool = Field(description="是否推荐")

# 2. 初始化大模型
llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V4-Flash",
    temperature=0,
    base_url=os.getenv("SILICON_BASE_URL"),
    api_key=os.getenv("SILICON_API_KEY")
)
# 3. 绑定结构化输出
structured_llm = llm.with_structured_output(schema=MovieReview)

# 4. 提示词
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是专业影评人，按要求返回结构化数据。"),
    ("human", "评价电影《{movie_name}》")
])

# 5. 组装 LCEL 链
chain = prompt | structured_llm

# 6. 调用
result = chain.invoke({"movie_name": "盗梦空间"})

# 7. 输出
print(f"电影: {result.title}")
print(f"评分: {result.rating}/10")
print(f"简介: {result.summary}")
print(f"推荐: {'是' if result.recommended else '否'}")
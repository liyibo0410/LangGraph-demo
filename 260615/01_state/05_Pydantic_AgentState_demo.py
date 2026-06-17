# 03_state/05_Pydantic_AgentState_demo.py

from typing import Optional
from pydantic import BaseModel, Field, field_validator
from datetime import datetime


# 1. 定义结构
class AgentState(BaseModel):
    """使用Pydantic BaseModel定义状态"""

    # 必需字段
    user_id: str = Field(description="用户唯一标识")
    query: str = Field(min_length=1, max_length=20, description="用户输入的查询")
    timestamp: datetime = Field(default_factory=datetime.now, description="状态创建时间")

    # 可选字段
    rag_result: Optional[str] = Field("abc", description="RAG检索结果")
    web_search_result: Optional[str] = Field(None, description="网络搜索结果")
    final_answer: Optional[str] = Field(None, description="最终回复")

    # 验证器
    @field_validator('query')
    @classmethod
    def validate_query_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("查询不能为空")
        return v.strip()


try:
    # 2. 实例化
    state = AgentState(
        user_id="user_123",
        query="LangGraph的State是什么",
        # rag_result="LangGraph通过StateGraph来管理状态...",
        web_search_result="根据官方文档，状态是LangGraph的核心概念..."
    )

    # 3. 数据访问
    print("Pydantic状态测试:")
    print(f"用户ID: {state.user_id}")
    print(f"查询: {state.query}")
    print(f"时间戳: {state.timestamp}")
    print(f"RAG结果: {state.rag_result}")

    # # 4. 转成dict
    # state_dict = 01_state.model_dump()
    # print(f"序列化后的字典: {state_dict}")

except ValueError as e:
    # 5. 测试验证器
    print(f"验证错误捕获: {e}")

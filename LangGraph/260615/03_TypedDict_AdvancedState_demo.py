
from typing import TypedDict, List, NotRequired, Dict


# 1. 定义结构
class AdvancedState(TypedDict):
    #必填字段
    user_query: str
    conversation_history: List[str]

    #可选字段: 字段可缺失
    rag_documents: NotRequired[List[Dict[str, str]]]
    web_search_results: NotRequired[List[str]]

# 2. 实例化状态
# 2.1 创建简单的状态
simple_state: AdvancedState = {
    "user_query": "大模型中的“幻觉”是什么意思？",
    "conversation_history": [
        "human：大模型中的“幻觉”是什么意思？",
        "AI：就是大模型胡说八道？"]
}

# 2.2 创建完整的状态
full_state: AdvancedState = {
    "user_query": "请解释LangGraph的状态管理",
    "conversation_history": ["你好，我是AI助手", "我能帮您了解LangGraph"],
    "rag_documents": [
        {"title": "LangGraph文档", "content": "状态管理章节..."},
        {"title": "最佳实践", "content": "TypedDict是推荐方式..."}
    ]
}
print(full_state)
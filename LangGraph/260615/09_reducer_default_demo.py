"""
Reducer的默认行为：覆盖
"""
import operator
from typing import TypedDict, List, Annotated

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, add_messages


# 1. 定义图状态 - 所有字段均未指定reducer，故默认为覆盖
class AgentState(TypedDict):
    query: str
    # 替换
    messages: List[BaseMessage]  # 历史消息列表
    search_results: List[str]    # 搜索结果列表

# 2. 节点函数：输入处理
def input_node(state: AgentState):
    query = state["query"]
    new_message = HumanMessage(content = f"用户问题：{query}" )

    return {"messages": [new_message]}

# 3. 节点函数：搜索处理
def search_node(state: AgentState):
    query = state["query"]
    #省略调用向量数据库
    query_result = f"模拟大模型返回的结果，关于“{query}”的相关信息....blabla"
    search_message = AIMessage(content = f"搜索完成：{query_result}" )

    return {"messages": [search_message], "search_results": [query_result]}

# 4. 节点函数：处理最终结果
def response_node(state: AgentState):
    query = state["query"]
    context = state["search_results"]

    # 组装最终结果
    final_response = f"基于大模型的搜索结果：“{query}”的回答是：{context}"
    ai_response = AIMessage(content = final_response)

    return {
        "messages": [ai_response],
        "search_results": [f"最终回复已生成"],
    }

# 5. 构建图
def build_graph():
    workflow = StateGraph(AgentState)

    # 添加节点
    workflow.add_node("input", input_node)
    workflow.add_node("search", search_node)
    workflow.add_node("response", response_node)

    # 设置边
    workflow.add_edge("input", "search")
    workflow.add_edge("search", "response")

    # 设置入口和出口
    workflow.set_entry_point("input")
    workflow.set_finish_point("response")

    return workflow.compile()

if __name__ == "__main__":

    #创建编译后的图实例
    app = build_graph()

    #初始化状态
    init_state = {
        "query": "如何实现年薪30万",
        "messages": [SystemMessage(content="你是一个职业规划师，请做专业的职业规划")],
        "search_results": []
    }

    final_state = app.invoke(init_state)

    print("=======用户问题========")
    print(f"查询：{final_state['query']}")

    print("=======消息历史========")
    for i, msg in enumerate(final_state["messages"]):
        print(f"{i} {msg.type} {msg.content}")

    print("=======搜索结果========")
    for i, res in enumerate(final_state["search_results"]):
        print(f"{i} {res}")


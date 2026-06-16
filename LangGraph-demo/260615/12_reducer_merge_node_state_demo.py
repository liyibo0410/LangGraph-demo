
"""
目标：节点状态合并
"""
import operator
import time
from typing import TypedDict, List, Annotated

from langgraph.constants import START, END
from langgraph.graph import StateGraph


# 1. 定义图状态(有key约束的字典类)
class MyState(TypedDict):
    query: str # 用户问题
    rag_result: str # rag搜索结果
    web_search_result: str # 网络搜索结果
    final_answer: str # 最终答案
    messages: Annotated[List[str], operator.add]

# 2. 定义节点函数
# 2.1 定义RAG搜索节点
def rag_search_node(state: MyState):

    # 1. 获取用户输入
    print("📚【技术知识库】开始检索学术定义...")
    query = state.get("query")

    # 2. 模拟RAG搜索（将问题向量化，然后去向量数据库做相似度比对，得到结果）
    time.sleep(2)
    rag_result = f"📚【学术定义】{query}：指大语言模型（LLM）生成的内容虽然看似合理且流畅，但实际上与源上下文或现实世界事实不符，甚至完全虚构的现象。"

    # 3 将搜索结果写入到图状态中
    print("📚【技术知识库】检索完成！")
    return {"rag_result": rag_result, "messages": ["hahaha"]}

# 2.2 定义网络搜索节点
def web_search_node(state: MyState):

    # 1. 获取用户输入
    print("🌏【网络搜索】开始检索网络最新内容...")
    query = state.get("query")

    # 2. 模拟网络搜索（MCP）
    time.sleep(2)
    web_search_result = f"🌏【网络搜索】{query}：支大模型胡说八道。"

    # 3 将搜索结果写入到图状态中
    print("🌏【网络搜索】检索完成！")
    return {"web_search_result": web_search_result, "messages": ["heiheihei"]}

# 2.3. 定义最终回复节点
def final_answer_node(state: MyState):

    # 1 从图状态中获取多路搜索结果
    print("🤖【AI助手】正在综合多方信息生成回答...")
    rag_result = state["rag_result"]
    web_search_result = state["web_search_result"]

    # 2 模拟调用大模型
    final_answer = f"""
🤖【AI助手总结】：
{rag_result}
{web_search_result}
以及大模型的一些其他回答
需要我教你如何降低模型的幻觉率吗❓
"""
    time.sleep(2)

    # 3 将最终回复写入到图状态中
    print("🤖【AI助手】回答生成结束！")
    return {"final_answer": final_answer}

# 3. 通过状态创建图实例
graph = StateGraph(MyState)

# 4. 添加节点
graph.add_node(rag_search_node)
graph.add_node(web_search_node)
graph.add_node(final_answer_node)

# 5. 添加边
graph.add_edge(START, "rag_search_node")
graph.add_edge(START, "web_search_node")
graph.add_edge("rag_search_node", "final_answer_node")
graph.add_edge("web_search_node", "final_answer_node")
graph.add_edge("final_answer_node", END)

# 6. 编译图
compiled_graph = graph.compile()

# 7. 启动工作流
#query从START传入
final_state = compiled_graph.invoke({"query": "大模型中的“幻觉”是什么意思"})

# 8. 输出结果
print(final_state)

# 9. 打印流程图（工作流）
compiled_graph.get_graph().print_ascii()
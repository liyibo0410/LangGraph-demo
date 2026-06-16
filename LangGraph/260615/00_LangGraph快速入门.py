# 导入time模块，用来模拟接口/知识库查询耗时，sleep模拟网络等待
import time
# TypedDict：类型字典，给LangGraph的全局状态做类型约束，规范状态里有哪些字段、是什么类型
from typing import TypedDict

# LangGraph内置常量：START代表流程图起点，END代表流程图终点
from langgraph.constants import START, END
# StateGraph：LangGraph核心类，用来构建基于状态流转的图工作流
from langgraph.graph import StateGraph

"""
项目目标：构建一个并行检索问答工作流
用户提问后，同时走【本地知识库RAG检索】+【全网实时搜索】两条并行分支
两条检索全部完成后，再汇总信息交给大模型生成最终回答
完整流程步骤：
1. 定义全局状态（整个图流转过程中共享的数据容器）
2. 定义每一个业务节点函数（每个节点是一段独立业务逻辑）
3. 使用状态类初始化图实例
4. 把所有业务节点注册到图中
5. 配置节点之间的流转边（定义执行顺序、并行逻辑）
6. 编译图，生成可调用的运行实例
7. 传入用户输入，启动整个工作流执行
8. 读取最终输出结果并打印
9. 打印ASCII流程图，直观查看结构
用户测试问题：大模型中的“幻觉”是什么意思？
"""

# ====================== 1. 定义图全局状态 MyState ======================
# 继承TypedDict，规定整个工作流全程共享的数据字段，所有节点都能读写这个状态
class MyState(TypedDict):
    query: str               # 用户原始提问，全程全局可用
    rag_result: str          # 本地知识库RAG检索返回的结果
    web_search_result: str   # 全网实时搜索返回的结果
    final_answer: str        # 汇总信息后大模型生成的最终回答

# ====================== 2. 定义所有业务节点函数 ======================
# 规则：LangGraph节点函数固定格式：入参只有state（当前全局状态），返回字典，字典key对应状态字段，用来更新状态
# 2.1 RAG知识库检索节点：读取用户问题，模拟本地知识库查询，把结果写入状态rag_result
def rag_search_node(state: MyState):
    # 打印日志，区分当前正在执行哪个节点，方便调试看流程顺序
    print("📚【技术知识库】开始检索学术定义...")
    # 从全局状态state中取出用户输入query
    query = state.get("query")

    # time.sleep(2) 模拟真实RAG向量库查询耗时，等待2秒
    time.sleep(2)
    # 模拟知识库返回的专业学术解释
    rag_result = f"📚【学术定义】{query}：指大语言模型（LLM）生成的内容虽然看似合理且流畅，但实际上与源上下文或现实世界事实不符，甚至完全虚构的现象。"

    print("📚【技术知识库】检索完成！")
    # 返回字典，key是rag_result，LangGraph会自动把这个值更新到全局状态MyState的rag_result字段
    return {"rag_result": rag_result}

# 2.2 全网实时搜索节点：并行执行，同时读取用户问题，模拟联网搜索
def web_search_node(state: MyState):
    print("🌏【实时网络搜索】全网查询最新案例...")
    # 另一种取状态字段写法：state["query"] 等价 state.get("query")，不存在key会直接报错
    query = state["query"]

    # 模拟联网搜索接口等待2秒
    time.sleep(2)
    # 模拟网络搜索得到的通俗案例解释
    web_search_result = f"🌏【通俗解释】{query}：常被戏称为AI在“一本正经地胡说八道”。比如AI可能会捏造不存在的历史事件、错误的代码库引用或虚假的论文出处。"

    print("🌏【实时网络搜索】搜索完毕！")
    # 更新全局状态的web_search_result字段
    return {"web_search_result": web_search_result}

# 2.3 汇总生成最终回答节点：必须等上面两个并行节点全部跑完才会执行
def final_answer_node(state: MyState):
    print("🤖【AI助手】正在综合多方信息生成回答...")
    # 从全局状态取出两个并行节点生成好的检索结果
    rag_result = state["rag_result"]
    web_search_result = state["web_search_result"]

    # 模拟大模型汇总两段信息生成最终回答
    final_answer = f"""
🤖【AI助手总结】：
{rag_result}
{web_search_result}
需要我教你如何降低模型的幻觉率吗❓
"""
    # 模拟大模型推理耗时2秒
    time.sleep(2)

    print("🤖【AI助手】回答生成结束！")
    # 更新全局状态的final_answer字段，存储最终回复
    return {"final_answer": final_answer}

# ====================== 3. 初始化状态图实例 ======================
# StateGraph(MyState)：创建图对象，绑定我们定义好的全局状态MyState，整个图所有节点共享这个状态
graph = StateGraph(MyState)

# ====================== 4. 向图中注册所有业务节点 ======================
# add_node(节点函数)：LangGraph会自动以【函数名】作为节点唯一标识字符串
# 这里三个节点标识分别是 "rag_search_node"、"web_search_node"、"final_answer_node"
graph.add_node(rag_search_node)
graph.add_node(web_search_node)
graph.add_node(final_answer_node)

# ====================== 5. 配置节点流转边（核心：定义并行逻辑） ======================
# add_edge(起点标识, 终点标识)：定义一条单向流转边，代表执行完起点后走向终点
# START是流程图内置起点，用户输入进来后同时分发到两个节点，实现并行
graph.add_edge(START, "rag_search_node")
graph.add_edge(START, "web_search_node")
# 两条并行节点都指向最终汇总节点：LangGraph默认等待所有前置节点全部执行完成，才会执行终点节点
graph.add_edge("rag_search_node", "final_answer_node")
graph.add_edge("web_search_node", "final_answer_node")
# 汇总节点执行完成后，流转到END流程图终点，整个工作流结束
graph.add_edge("final_answer_node", END)

# ====================== 6. 编译图，生成可运行实例 ======================
# compile()：把上面定义好的节点、边、状态编译成可调用、可执行的工作流对象
compiled_graph = graph.compile()

# ====================== 7. 启动工作流，传入初始输入 ======================
# invoke(初始状态字典)：触发图执行，传入初始全局状态，只需要提供初始必须的query字段
# type:# ignore[arg-type]是pylint类型忽略注释，消除静态类型警告
state = compiled_graph.invoke({"query": "大模型中的“幻觉”是什么意思？"}) # type: ignore[arg-type]

# ====================== 8. 读取并打印最终结果 ======================
# state是执行完成后的完整全局状态字典，取出final_answer打印输出
print("\n========== 最终回答 ==========")
print(state["final_answer"])

# ====================== 9. 打印ASCII文本流程图，可视化结构 ======================
# get_graph() 获取图结构，print_ascii() 在控制台打印字符流程图
print("\n========== 流程图结构 ==========")
compiled_graph.get_graph().print_ascii()

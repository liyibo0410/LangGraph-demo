# 03_state/14_langgraph_checkpointer_demo.py
"""
LangGraph 状态存储示例：使用 Checkpointer 持久化会话上下文记忆
核心知识点：
1. MemorySaver：内存级检查点存储，程序重启后数据丢失，仅用于本地测试
2. thread_id：会话唯一标识，相同thread_id共享一份状态，不同thread_id状态隔离
3. Annotated[List[str], operator.add]：状态字段合并策略，多次调用自动追加列表内容而非覆盖
4. compile(checkpointer=xxx)：给图挂载状态持久化能力，每次运行自动读写状态快照
"""

# 导入运算符，用于定义状态列表字段的合并规则（追加而非覆盖）
import operator
# 类型注解工具：TypedDict定义图全局状态结构、List标注列表类型、Annotated附加合并规则
from typing import TypedDict, List, Annotated

# LangGraph 内存检查点组件：临时存储每个会话的状态快照
from langgraph.checkpoint.memory import MemorySaver
# 常量：START图起始节点、END图终止节点
from langgraph.constants import END, START
# 状态图核心构建类 StateGraph
from langgraph.graph import StateGraph


# ====================== 1. 定义图全局状态 AgentState ======================
# TypedDict：定义贯穿整个图所有节点的统一全局状态，所有节点读写同一份state
class AgentState(TypedDict):
    # 用户单次输入的提问文本，每次invoke会传入新query覆盖此字段
    query: str
    # 对话上下文摘要列表
    # Annotated[列表类型, operator.add] 关键：多次执行节点时，新列表会自动追加到原有列表尾部，不会直接覆盖
    current_context: Annotated[List[str], operator.add]


# ====================== 2. 定义业务节点函数 echo_node ======================
# 图中唯一业务节点：接收全局状态，处理对话并更新上下文记忆
# 入参 state：当前会话加载到的全局 AgentState 状态
def echo_node(state: AgentState):
    # 从全局状态中取出本次用户输入的问题
    query = state["query"]

    # 模拟对话摘要逻辑：把本次用户提问封装成一条上下文记录
    new_context = f"最近一次交流: {query}"

    # 返回字典，对应要更新的状态字段
    # 因为current_context配置了operator.add，这里返回列表[new_context]会自动追加到历史列表，不会覆盖原有内容
    return {
        "current_context": [new_context]
    }


# ====================== 3. 构建完整流程图 ======================
def build_graph():
    # 实例化状态图，绑定全局状态结构 AgentState
    workflow = StateGraph(AgentState)
    # 向图中注册节点：节点名称"echo"，绑定处理函数echo_node
    workflow.add_node("echo", echo_node)
    # 添加边：图起始节点 START → 业务节点 echo
    workflow.add_edge(START, "echo")
    # 添加边：业务节点 echo → 终止节点 END，执行完echo直接结束单次流程
    workflow.add_edge("echo", END)
    # 返回未编译的原始图对象，后续挂载检查点后编译才能运行
    return workflow


# ====================== 4. 主演示逻辑 ======================
def demo_langgraph():
    # 1. 实例化内存检查点存储器
    # MemorySaver 仅存在内存中，程序关闭所有会话状态全部清空；生产环境需替换Redis/SQL持久化存储
    checkpointer = MemorySaver()

    # 2. 获取构建好的原始流程图
    graph = build_graph()

    # 3. 编译图，挂载检查点存储，开启会话状态持久化能力
    # 不传入checkpointer则每次invoke都会重置状态，无法保存会话历史
    app = graph.compile(checkpointer=checkpointer)

    # -------------------------- 测试1：同一会话第一次调用 --------------------------
    print("--- 第一次调用 ---")
    # invoke 执行单次图流程
    # input：本次流程传入的初始状态数据，本次只传入用户提问query
    # config：会话配置，configurable.thread_id 是会话唯一标识，用于区分不同用户/不同聊天窗口
    result1 = app.invoke(
        input={"query": "问题1"},
        config={"configurable": {"thread_id": "user_session1"}}
    )
    # 打印执行完成后的全局状态里的上下文列表
    print("第一次当前上下文:", result1["current_context"])

    # -------------------------- 测试2：同thread_id，同一会话第二次调用 --------------------------
    print("\n--- 第二次调用 (同一会话) ---")
    # 复用同一个 thread_id = user_session1，检查点会自动加载上一轮执行后的完整状态
    # 无需手动传入历史current_context，框架自动从MemorySaver读取会话快照
    result2 = app.invoke(
        input={"query": "问题2"},
        config={"configurable": {"thread_id": "user_session1"}}  # 和上一轮完全相同的会话ID
    )
    print("第二次当前上下文:", result2["current_context"])

    # -------------------------- 测试3：全新thread_id，开启独立新会话 --------------------------
    print("\n--- 第三次调用 (新会话) ---")
    # 更换全新会话ID，框架会创建一份全新独立状态，和user_session1的上下文完全隔离互不干扰
    new_thread_id = "user_session2"
    result3 = app.invoke(
        input={"query": '问题3'},  # 新会话第一条提问
        config={"configurable": {"thread_id": new_thread_id}}  # 全新会话标识
    )
    print("新会话当前上下文:", result3["current_context"])


# 程序入口：脚本直接运行时执行演示函数
if __name__ == "__main__":
    demo_langgraph()




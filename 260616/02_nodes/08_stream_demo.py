# 04_nodes/08_stream_demo.py
import time
from typing import TypedDict, Annotated, List
import operator

# LangChain LLM 初始化、消息封装相关
from langchain.chat_models import init_chat_model
from langchain_core.messages import BaseMessage, HumanMessage
# LangGraph 核心图、运行时、流式组件
from langgraph.graph import StateGraph, START, END
from langgraph.runtime import Runtime

# 外部配置文件，存放大模型地址、密钥、模型名等
from lm_config import lm_config

# ====================== 全局初始化LLM大模型 ======================
llm_client = init_chat_model(
    model=lm_config.llm_model,               # 使用的大模型名称
    model_provider=lm_config.model_provider, # 厂商类型 openai / deepseek / 通义千问等
    base_url=lm_config.base_url,             # 接口代理/私有部署地址
    api_key=lm_config.api_key,               # 模型密钥
)

# ====================== 1. 定义图全局状态 State ======================
class State(TypedDict):
    input: str  # 用户原始输入提问
    # Annotated + operator.add：消息列表累加器，新消息自动追加不覆盖旧消息
    messages: Annotated[List[BaseMessage], operator.add]
    current_step: str  # 标记当前走到哪个流程步骤

# ====================== 2. 节点1：接收用户输入 ======================
def node_input(state: State):
    """接收用户输入，把用户提问包装成人类消息存入消息列表"""
    input_text = state["input"]
    return {
        # 增量追加一条用户消息
        "messages": [HumanMessage(content=input_text)],
        "current_step": "接收用户输入"
    }

# ====================== 3. 节点2：中间处理节点（自定义流式custom数据源） ======================
def node_processing(state: State, runtime: Runtime):
    """
    模拟RAG前置处理：意图识别、知识库检索、Prompt组装
    依赖 runtime.stream_writer 向外推送自定义流式数据
    仅 stream_mode="custom" 能捕获 writer 发送的数据，不改动全局State
    """
    # 模拟三段处理步骤
    steps = ["正在分析意图...", "正在检索知识库...", "正在构建Prompt..."]
    # 获取流式写入器，用于推送自定义实时信息
    writer = runtime.stream_writer

    for i, step in enumerate(steps):
        time.sleep(0.5)  # 模拟接口/计算耗时

        # 向外发送自定义流式数据包，前端可实时展示进度条、步骤提示
        writer({
            "step_index": i + 1,
            "description": step,
            "timestamp": time.time()
        })

    # 仅更新步骤状态，无自定义状态输出
    return {"current_step": "处理完成"}

# ====================== 4. 节点3：LLM生成答案（原生token流式） ======================
def node_generation(state: State):
    """
    调用大模型生成回答，LangGraph自动捕获LLM逐字流式token
    stream_mode="messages" 专门用来接收大模型打字机式输出
    """
    # 传入历史完整对话消息给LLM
    response = llm_client.invoke(state["messages"])

    # 将AI回复追加进消息列表，更新流程标记
    return {
        "messages": [response],
        "current_step": "生成完成"
    }

# ====================== 5. 搭建流程图 ======================
def build_graph():
    graph = StateGraph(State)
    # 注册三个业务节点
    graph.add_node("input", node_input)
    graph.add_node("process", node_processing)
    graph.add_node("generate", node_generation)

    # 串行流程：起点 → 接收输入 → 预处理 → LLM生成 → 结束
    graph.add_edge(START, "input")
    graph.add_edge("input", "process")
    graph.add_edge("process", "generate")
    graph.add_edge("generate", END)

    # 编译生成可运行应用
    return graph.compile()

# ====================== 6. 五种流式模式 + 混合模式完整演示 ======================
def demo_langgraph():
    # 初始化状态：用户提问、空消息列表、初始步骤标记
    initial_state = {"input": "我是谁", "messages": [], "current_step": "start"}
    app = build_graph()

    # --------------------------
    # 模式1：values 完整状态输出
    # 每走完一个节点，返回当前完整的全部state
    # --------------------------
    print(f"\n{'=' * 20} 1. Mode: values {'=' * 20}")
    print("描述: 每执行完一个节点，输出当前完整State全部字段")
    for event in app.stream(initial_state, stream_mode="values"):
        print(f"State完整数据: {event}")

    # --------------------------
    # 模式2：updates 增量更新输出
    # 只输出当前节点return返回的增量字典，不包含未修改字段，数据更轻量
    # --------------------------
    print(f"\n{'=' * 20} 2. Mode: updates {'=' * 20}")
    print("描述: 仅输出当前节点修改的增量字段，体积更小")
    for event in app.stream(initial_state, stream_mode="updates"):
        print(f"增量更新内容: {event}")

    # --------------------------
    # 模式3：custom 自定义流式数据
    # 仅捕获 runtime.stream_writer() 手动推送的自定义消息，和状态无关
    # 适合推送进度、日志、中间提示词
    # --------------------------
    print(f"\n{'=' * 20} 3. Mode: custom {'=' * 20}")
    print("描述: 只接收节点内writer手动推送的自定义实时步骤信息")
    for event in app.stream(initial_state, stream_mode="custom"):
        print(f"自定义流式数据: {event}")

    # --------------------------
    # 模式4：messages LLM token流式输出
    # 专门捕获大模型逐块返回的文字token，实现打字机效果对话
    # --------------------------
    print(f"\n{'=' * 20} 4. Mode: messages {'=' * 20}")
    print("描述: 实时输出LLM逐字生成的Token片段")
    for chunk, metadata in app.stream(initial_state, stream_mode="messages"):
        node_name = metadata.get('langgraph_node', 'unknown')
        # 实时打印AI输出文字
        print(f"[{node_name}] Token片段: {chunk.content!r}", end="")
        time.sleep(0.1)

    # --------------------------
    # 模式5：debug 全量调试模式
    # 输出完整运行日志：节点进入、退出、状态变更、异常、缓存、重试等全部事件
    # 开发排错专用，生产环境不推荐
    # --------------------------
    print(f"\n\n{'=' * 20} 5. Mode: debug {'=' * 20}")
    print("描述: 输出完整底层执行调试日志，排查流程bug专用")
    count = 0
    for event in app.stream(initial_state, stream_mode="debug"):
        if count < 3:  # 只打印前3条避免刷屏
            print(f"Debug事件类型: {event['type']} | 节点: {event.get('payload', {}).get('name')}")
        count += 1
    print("... (省略后续大量debug日志)")

    # --------------------------
    # 模式6：混合模式 同时监听多种流
    # stream_mode传列表，可一次性接收 updates + custom 等多种数据
    # 返回 (mode名称, 对应数据) 二元组
    # --------------------------
    print(f"\n{'=' * 20} 6. Mixed Mode 混合流式 {'=' * 20}")
    print("描述: 同时监听增量状态更新 + 自定义步骤消息")
    for mode, data in app.stream(initial_state, stream_mode=["updates", "custom"]):
        if mode == "updates":
            # updates数据：key是节点名
            node_key = list(data.keys())[0]
            print(f"[增量状态] 来自节点: {node_key}")
        elif mode == "custom":
            print(f"[流程提示] {data['description']}")


# 程序入口执行演示
if __name__ == "__main__":
    demo_langgraph()
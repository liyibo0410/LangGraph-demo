# 04_nodes/07_node_default_retry_demo.py
from typing import Dict, Any

# 导入LangGraph图构建、起止节点、重试策略类
from langgraph.graph import StateGraph, START, END
from langgraph.types import RetryPolicy
# 用于定义图状态结构
from typing_extensions import TypedDict


# ====================== 1. 定义图全局状态 ======================
class State(TypedDict):
    result: str  # 存储API调用成功后的返回文本


# ====================== 2. 模拟不稳定易报错的API节点 ======================
# 全局变量：记录当前总共发起了多少次接口调用
attempt_counter = 0

def unstable_node(state: State) -> Dict[str, Any]:
    """
    模拟不稳定第三方API/LLM接口：前2次主动抛异常失败，第3次正常返回
    global 声明使用外部全局计数器，统计重试次数
    """
    global attempt_counter
    # 每进入一次节点，尝试次数+1
    attempt_counter += 1
    print(f"尝试调用API，这是第 {attempt_counter} 次尝试")

    # 逻辑：前2次直接抛出异常模拟接口报错
    if attempt_counter < 3:
        raise Exception(f"模拟API调用失败 (尝试 {attempt_counter})")
    else:
        # 第3次调用成功，返回更新后的状态字段
        return {
            "result": f"API调用成功，经过 {attempt_counter} 次尝试"
        }


# ====================== 3. 搭建并编译流程图 ======================
def build_graph():
    # 初始化状态图，绑定自定义State
    graph = StateGraph(State)

    # 注册不稳定节点，配置重试策略
    # retry_policy=RetryPolicy(max_attempts=5)
    # max_attempts=5：该节点最多自动重试5次（包含第一次原始执行）
    graph.add_node(
        "unstable_node",
        unstable_node,
        retry_policy=RetryPolicy(max_attempts=5)
    )

    # 流程流向：起点 → 不稳定接口节点 → 流程结束
    graph.add_edge(START, "unstable_node")
    graph.add_edge("unstable_node", END)

    # 编译生成可执行的图应用
    return graph.compile()


# ====================== 4. 重试演示主逻辑 ======================
def demo_langgraph():
    global attempt_counter
    # 每次运行前重置计数器，避免上次运行数据干扰
    attempt_counter = 0

    app = build_graph()
    try:
        # 发起图执行，传入初始空状态
        result = app.invoke({"result": ""})
        print(f"最终结果: {result}\n")
    except Exception as e:
        # 若达到最大重试次数仍失败，会捕获最终抛出的异常
        print(f"最终失败: {type(e).__name__}: {e}\n")


# 程序入口
if __name__ == "__main__":
    demo_langgraph()
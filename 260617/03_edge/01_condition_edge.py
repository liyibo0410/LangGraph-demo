# 05_edge/01_condition_edge.py
from typing import Literal
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

# ====================== 1. 定义图全局状态 ======================
class GraphState(TypedDict):
    value: int   # 用于判断奇偶的数字，分支判断依据
    step: str    # 记录当前执行到哪一步节点

# ====================== 2. 定义三个业务节点 ======================
def node_a(state: GraphState) -> dict:
    """节点A：前置统一处理节点，所有流程都先执行A"""
    print("执行节点A")
    # 直接把原值和步骤标识写入状态
    return {"value": state["value"], "step": "A执行完毕"}

def node_b(state: GraphState) -> dict:
    """节点B：偶数分支专属处理逻辑"""
    print("执行节点B")
    # 偶数 ×2
    return {"value": state["value"] * 2, "step": "B执行完毕"}

def node_c(state: GraphState) -> dict:
    """节点C：奇数分支专属处理逻辑"""
    print("执行节点C")
    # 奇数 -1
    return {"value": state["value"] - 1, "step": "C执行完毕"}

# ====================== 3. 条件路由判断函数（分支核心） ======================
def route_condition(state: GraphState) -> Literal["node_b_alias", "node_c_alias"]:
    """
    接收当前全局状态，根据条件返回分支别名
    Literal 约束返回值只能是两个指定字符串，代码提示更友好
    返回的不是真实节点名，是自定义别名，需要path_map映射对应真实节点
    """
    if state["value"] % 2 == 0:
        return "node_b_alias"  # 偶数 → 匹配别名node_b_alias
    else:
        return "node_c_alias"  # 奇数 → 匹配别名node_c_alias

# ====================== 4. 搭建流程图、配置条件分支 ======================
def build_graph():
    # 初始化状态图，绑定自定义状态GraphState
    graph = StateGraph(GraphState)

    # 注册节点，键为节点真实名称
    graph.add_node("node_a", node_a)
    graph.add_node("node_b", node_b)
    graph.add_node("node_c", node_c)

    # 固定直线边：流程起点 START 直接走到 node_a
    graph.add_edge(START, "node_a")

    # ========== 重点：添加条件分支边 add_conditional_edges ==========
    # 参数1：source 源节点，从哪个节点分出分支（这里是node_a执行完后分支）
    # 参数2：path 路由判断函数，用来计算走哪条分支
    # 参数3：path_map 映射字典 {路由返回别名: 真实节点名称}
    graph.add_conditional_edges(
        source="node_a",
        path=route_condition,
        path_map={
            "node_b_alias": "node_b",
            "node_c_alias": "node_c"
        }
    )

    # 两条分支最终都指向结束节点END
    graph.add_edge("node_b", END)
    graph.add_edge("node_c", END)

    # 编译图，生成可调用实例
    return graph.compile()

# ====================== 5. 程序入口，测试奇偶两种分支 ======================
if __name__ == "__main__":
    app = build_graph()

    # 测试1：偶数输入 2 → 走 node_b
    print("\n输入值为偶数 (2):")
    result = app.invoke({"value": 2})
    print(f"执行结果: {result}")

    # 测试2：奇数输入 1 → 走 node_c
    print("\n输入值为奇数 (1):")
    result = app.invoke({"value": 1})
    print(f"执行结果: {result}")
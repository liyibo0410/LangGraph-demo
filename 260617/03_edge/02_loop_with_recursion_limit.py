# 05_edges/02_loop_with_recursion_limit.py
from typing import Literal
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
# 循环步数超限专属异常类
from langgraph.errors import GraphRecursionError

# ====================== 1. 定义图全局状态 ======================
class LoopState(TypedDict):
    count: int        # 循环计数器，记录当前循环次数
    result: str       # 存储每轮循环的日志文本
    max_count: int    # 业务自定义终止阈值，达到该数字正常退出循环

# ====================== 2. 定义两个循环节点 ======================
def node_a(state: LoopState) -> dict:
    """主业务处理节点：每次执行计数器+1，更新日志"""
    print(f"执行节点A，当前计数: {state['count']}")
    # 只返回需要更新的字段，LangGraph自动合并state
    return {
        'count': state['count'] + 1,
        'result': f"已处理 {state['count']} 次"
    }

def node_b(state: LoopState) -> dict:
    """辅助处理节点，执行完会回流到node_a，构成循环闭环"""
    print(f"执行节点B，当前计数: {state['count']}")
    return {
        'result': f"已处理 {state['count']} 次 - 辅助处理"
    }

# ====================== 3. 循环条件路由函数 ======================
def route(state: LoopState) -> Literal["b", END]:
    """
    node_a执行完成后走该分支判断：
    1. 当前计数 >= 业务最大次数：返回END，流程直接结束
    2. 未达到阈值：返回"b"，跳转到辅助节点，之后回流node_a继续循环
    """
    if state['count'] >= state['max_count']:
        print(f"结束循环。")
        return END
    else:
        print(f"继续循环...")
        return "b"

# ====================== 4. 搭建循环流程图 ======================
def build_graph():
    # 初始化状态图，绑定自定义LoopState
    graph = StateGraph(LoopState)
    # 注册节点，简写节点标识 a / b
    graph.add_node("a", node_a)
    graph.add_node("b", node_b)

    # 流程链路搭建
    graph.add_edge(START, "a")               # 程序起点直接进入主节点a
    graph.add_conditional_edges("a", route)  # a执行完毕，走条件分支判断
    graph.add_edge("b", "a")                 # 辅助节点执行完，强制回到a，形成循环

    # 编译生成可运行的图实例
    return graph.compile()

# ====================== 5. 主程序运行演示 ======================
if __name__ == "__main__":
    app = build_graph()

    try:
        # 初始状态：计数器从0开始，业务需要循环到count=10才会主动结束
        input_data = {
            'count': 0,
            'max_count': 10
        }
        # recursion_limit：LangGraph底层安全保护，限制整张图最大执行节点步数
        # 作用：防止代码bug造成死循环无限运行，默认值25
        run_config = {
            'recursion_limit': 60  # 设置最大允许执行60步，远大于业务需要的步数，不会触发报错
        }
        # 执行流程图
        result = app.invoke(input=input_data, config=run_config)

        print("=== 执行成功 ===")
        print(result)

    except GraphRecursionError as e:
        # 若实际执行总节点步数超过recursion_limit，捕获该异常
        print(f"\n[系统警告] 捕获到递归错误: {e}")
        print("原因：图执行步数超过了 config 中设定的 recursion_limit。")
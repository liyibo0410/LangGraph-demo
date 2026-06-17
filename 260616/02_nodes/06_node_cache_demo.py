# 04_nodes/06_node_cache_demo.py
import time  # 用于模拟耗时计算、睡眠等待

# 导入LangGraph缓存、流程相关工具
from langgraph.cache.memory import InMemoryCache  # 内存缓存实现类
from langgraph.constants import START, END         # 图起始、结束常量
from langgraph.graph import StateGraph             # 状态图核心构建类
from langgraph.types import CachePolicy            # 缓存策略配置类
from typing_extensions import TypedDict            # 定义状态结构


# ====================== 1. 定义整张图共享的状态 ======================
class State(TypedDict):
    x: int       # 输入数字，作为节点计算参数、缓存key的依据
    result: int  # 节点计算输出结果


# ====================== 2. 模拟高耗时计算节点 ======================
def expensive_node(state: State) -> dict[str, int]:
    """
    模拟需要大量耗时/调用LLM/调用第三方接口的昂贵节点
    逻辑：输入x，返回 x*2
    """
    print(f"expensive_node 被调用")
    # 模拟耗时5秒的复杂运算、大模型调用、网络请求
    time.sleep(5)
    print(f"expensive_node 计算完成")

    # 只返回需要更新的字段
    return {"result": state["x"] * 2}


# ====================== 3. 搭建流程图结构 ======================
def build_graph():
    # 实例化状态图，绑定自定义状态State
    graph = StateGraph(State)

    # 注册节点，并配置节点专属缓存策略
    # cache_policy=CachePolicy(ttl=10)：该节点计算结果缓存有效期10秒
    graph.add_node(
        "expensive_node",
        expensive_node,
        cache_policy=CachePolicy(ttl=10)
    )

    # 设置流程走向：起点 → 昂贵计算节点 → 结束
    graph.add_edge(START, "expensive_node")
    graph.add_edge("expensive_node", END)
    return graph


# ====================== 4. 缓存完整演示逻辑 ======================
def demo_langgraph():
    # 1. 构建空白流程图
    graph = build_graph()

    # 2. 编译图，全局挂载内存缓存 InMemoryCache
    # 作用：所有带缓存策略的节点，计算结果都会存在这个内存缓存中
    # 生产环境可替换 RedisCache 实现分布式缓存
    app = graph.compile(cache=InMemoryCache())

    # 3. 第一次执行，输入x=5
    # 缓存中无记录，会真实执行 expensive_node，阻塞5秒
    print("===== 第一次执行 x=5 =====")
    print(app.invoke({"x": 5}))

    # 等待3秒（小于缓存有效期10秒）
    time.sleep(3)

    # 4. 第二次执行，同样输入x=5
    # 输入状态完全一致、且缓存未过期，直接读取缓存返回结果
    # 不会打印"被调用/计算完成"，不会sleep 5秒，瞬间返回
    print("\n===== 第二次执行 x=5（命中缓存） =====")
    print(app.invoke({"x": 5}))


# 程序入口
if __name__ == "__main__":
    demo_langgraph()
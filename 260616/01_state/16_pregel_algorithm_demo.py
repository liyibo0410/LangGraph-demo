# 03_state/16_pregel_algorithm_demo.py
# 导入operator工具，operator.add用于实现列表自动拼接合并
import operator
# Annotated：给状态字段附加额外规则（这里用来指定数据合并方式）
from typing import Annotated
# TypedDict：定义统一的状态字典结构，约束流程图中流转的数据格式
from typing_extensions import TypedDict
# LangGraph核心类
# StateGraph：用来搭建流程图的主类
# START：流程图固定起点标识（虚拟节点，不用自己写函数）
# END：流程图固定终点标识（走到这里流程结束）
from langgraph.graph import StateGraph, START, END

# ====================== 1. 定义整张图全局共用的状态 ======================
class State(TypedDict):
    # aggregate：用来收集所有节点输出内容的列表
    # Annotated[变量类型, 合并规则]
    # operator.add 代表：多个节点同时返回列表时，自动相加拼接，不会覆盖原有数据
    aggregate: Annotated[list, operator.add]

# ====================== 2. 定义流程图里每一个节点执行函数 ======================
# 所有节点函数固定两个入参：
# 01_state：当前全局最新状态
# config：执行配置（可忽略，这里仅占位）
# 返回值必须是字典，只会更新字典里写的字段，其他状态数据保留
def a(state: State, config):
    # 打印日志，查看执行时当前列表已有哪些内容
    print(f'Adding "A" to {state["aggregate"]}')
    # 节点a输出["A"]，会按照operator.add规则拼接到全局aggregate列表
    return {"aggregate": ["A"]}

def b(state: State, config):
    print(f'Adding "B" to {state["aggregate"]}')
    return {"aggregate": ["B"]}

def c(state: State, config):
    print(f'Adding "C" to {state["aggregate"]}')
    return {"aggregate": ["C"]}

def b_2(state: State, config):
    print(f'Adding "B_2" to {state["aggregate"]}')
    return {"aggregate": ["B_2"]}

def d(state: State, config):
    print(f'Adding "D" to {state["aggregate"]}')
    return {"aggregate": ["D"]}

# ====================== 3. 创建流程图对象，并注册所有节点 ======================
# 绑定上面定义的State状态结构，初始化空白流程图
graph = StateGraph(State)
# add_node("节点名称字符串", 对应执行函数)
# 作用：给一段逻辑起名字，后续连线靠名字关联
graph.add_node("a", a)
graph.add_node("b", b)
graph.add_node("b_2", b_2)
graph.add_node("c", c)
graph.add_node("d", d)

# ====================== 4. 添加节点流向边，定义执行顺序与分支 ======================
# add_edge(起点节点, 终点节点)：代表起点执行完后，走到终点节点
graph.add_edge(START, "a")        # 程序启动，第一个运行a节点
graph.add_edge("a", "b")         # a执行完毕，开启分支b
graph.add_edge("a", "c")         # a执行完毕，同时并行开启分支c
graph.add_edge("b", "b_2")       # b运行完，执行b_2
graph.add_edge("b_2", "d")       # b_2完成，等待另一条分支汇合
graph.add_edge("c", "d")         # c完成，等待另一条分支汇合
graph.add_edge("d", END)         # d执行完成，整张图运行结束

# 流程图执行逻辑拆解（Pregel多分支等待机制）：
# 1. START → a 串行执行a
# 2. a结束后，b 和 c 两个分支并行同时运行
# 3. 分支1：b → b_2；分支2：c
# 4. d节点有两个上游（b_2、c），必须两条分支全部跑完，才会执行d
# 5. d执行完走到END，流程终止

# ====================== 5. 编译流程图，生成可运行实例 ======================
# compile()：把节点、边、状态规则编译成可调用的运行对象
app = graph.compile()

# ====================== 6. 启动运行流程图 ======================
# invoke(初始状态)：同步阻塞运行整张图
# {"aggregate": []}：初始化全局列表为空
output_state = app.invoke({"aggregate": []})
# 打印所有节点跑完后的最终全局状态
print('执行图后的状态为', output_state, end="\n\n")

# ====================== 7. 打印图内所有注册节点对象 ======================
# app.01_state 是字典，key=节点名，value=节点底层完整信息
print('当前图的节点为', app.nodes, end="\n\n")

# ====================== 8. 打印状态通道channels ======================
# channels：管理状态每个字段，存储字段类型、合并规则、缓存数据
# 本代码只有一个通道aggregate，合并规则为列表相加
print('当前图的channels为', app.channels, end="\n\n")

# ====================== 9. 查看a节点底层属性（LangGraph底层Pregel机制） ======================
# triggers：触发该节点运行的上游依赖节点集合
# writers：会修改、写入当前状态通道的节点集合
print('节点a的triggers为', app.nodes['a'].triggers, end="\n\n")
print('节点a的writers为', app.nodes['a'].writers, end="\n\n")

# ====================== 10. 查看d节点底层依赖与写入信息 ======================
print('当前图的节点d的triggers为', app.nodes['d'].triggers, end="\n\n")
print('当前图的节点d的writers为', app.nodes['d'].writers, end="\n\n")
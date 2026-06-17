# 03_state/17_state_history_demo.py
# operator.add：实现list状态自动拼接，不覆盖
import operator
# os模块：创建文件夹，管理文件路径
import os
# Annotated：给状态字段附加合并规则
from typing import Annotated
# TypedDict：定义流程图全局状态结构
from typing_extensions import TypedDict
# LangGraph流程图核心组件
from langgraph.graph import StateGraph, START, END
# SqliteSaver：基于sqlite数据库的持久化存储器（保存每一步状态历史）
from langgraph.checkpoint.sqlite import SqliteSaver
# sqlite3：Python原生数据库驱动，用来连接本地sqlite文件
import sqlite3

# ====================== 1. 定义整张图全局共享状态 ======================
class State(TypedDict):
    # aggregate：列表存储每个节点输出标记
    # operator.add：多节点并行输出时自动列表相加，不会覆盖旧数据
    aggregate: Annotated[list, operator.add]

# ====================== 2. 定义各个节点执行函数 ======================
# 所有节点统一参数：01_state=当前全局状态，config=运行配置
# 返回字典，仅更新指定状态字段
def a(state: State, config):
    print(f'Adding "A" to {state["aggregate"]}')
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

# ====================== 3. 初始化流程图并注册节点 ======================
# 根据State结构创建空白流程图
graph = StateGraph(State)
# 绑定节点名称和对应执行函数
graph.add_node("a", a)
graph.add_node("b", b)
graph.add_node("b_2", b_2)
graph.add_node("c", c)
graph.add_node("d", d)

# ====================== 4. 搭建节点流向，定义并行分支逻辑 ======================
# START入口 -> a执行
graph.add_edge(START, "a")
# a执行完同时并行走两条分支 b、c
graph.add_edge("a", "b")
graph.add_edge("a", "c")
# 分支1：b执行完执行b_2
graph.add_edge("b", "b_2")
# b_2完成后等待c分支汇合到d
graph.add_edge("b_2", "d")
# c完成后等待b_2分支汇合到d
graph.add_edge("c", "d")
# d执行完毕流程结束
graph.add_edge("d", END)

# ====================== 5. 配置持久化存储：Sqlite检查点 ======================
# 创建存放数据库文件的文件夹，exist_ok=True文件夹存在也不报错
os.makedirs("sqlite_data", exist_ok=True)
# 连接本地sqlite数据库文件
# check_same_thread=False：多线程场景兼容，单脚本运行可加
conn = sqlite3.connect(database="./sqlite_data/checkpointer.db", check_same_thread=False)
# 用数据库连接创建LangGraph持久化存储器
# 作用：每执行完一个节点，自动把当前状态存入数据库，永久保存历史
checkpointer = SqliteSaver(conn)

# 编译流程图，关键：传入checkpointer开启状态持久化、历史记录功能
app = graph.compile(checkpointer=checkpointer)

# ====================== 6. 启动执行流程图 ======================
# invoke({}, ...)：初始状态不传参数，内部会自动初始化为空列表
# config={'configurable': {'thread_id': '1'}}
# thread_id：会话唯一标识，同一个thread_id的所有运行步骤会存在一组历史里
# 不同thread_id代表独立会话，数据互不干扰
output_state = app.invoke({}, config={'configurable': {'thread_id': '1'}})

# ====================== 7. 读取状态与历史记录 ======================
# 打印流程全部跑完后的最终状态
print(output_state)

# get_state_history：读取该thread_id下每一步的完整状态历史（迭代器）
all_states = app.get_state_history(config={'configurable': {'thread_id': '1'}})
# 迭代器转列表，方便循环打印每一步记录
all_states_list = list(all_states)

print("历史所有状态如下：\n")
# 循环打印每一步节点执行后的快照、元数据、步骤序号
for state in all_states_list:
    print(state, end="\n" + "="*30 + "\n")

print("\n\n最近一次状态如下：\n")
# get_state：只获取当前会话最新的最终状态快照
last_state = app.get_state(config={'configurable': {'thread_id': '1'}})
print(last_state)
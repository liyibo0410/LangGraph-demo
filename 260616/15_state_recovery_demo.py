"""
LangGraph 状态存储示例：从 checkpointer 中恢复状态
【整体功能说明】
这段代码演示了 LangGraph 最核心的「断点续跑」能力：
1. 把图运行过程中的每一步状态，保存到 SQLite 数据库里（相当于游戏存档）
2. 如果程序中途崩溃/报错，修复后可以从崩溃的位置继续执行，不用从头开始
3. 核心依赖：SqliteSaver 检查点保存器 + thread_id 会话标识
"""

# ========== 1. 导入需要的工具库 ==========
# os 是 Python 内置库，用来操作文件/文件夹，这里用来创建存数据库的文件夹
import os
# sqlite3 是 Python 内置的 SQLite 数据库操作库，用来连接本地数据库文件
import sqlite3
# TypedDict 用来给字典定义固定的字段和类型，让我们的「状态」结构更清晰、不容易写错
from typing import TypedDict

# 从 langgraph 的 SQLite 检查点模块，导入 SqliteSaver
# SqliteSaver 是核心工具：负责把图的运行状态「存进 SQLite 数据库」，也能从数据库里读出来恢复
# 【小白类比】它就是游戏的「存档/读档管理器」
from langgraph.checkpoint.sqlite import SqliteSaver
# END 是 LangGraph 的固定常量，代表图的「终点节点」，流程走到这里就结束了
from langgraph.constants import END
# START 是 LangGraph 的固定常量，代表图的「起点节点」，流程从这里开始
from langgraph.graph import START
# StateGraph 是 LangGraph 最核心的「状态图」类，用来搭建我们的工作流节点和流程
from langgraph.graph import StateGraph


# ========== 2. 定义图的「状态」结构 ==========
"""
【状态是什么？】
状态就是整个工作流里，所有节点共享的「全局数据容器」。
每个节点执行时，都可以读取状态里的数据，也可以返回新数据去更新状态。
就像接力赛的接力棒，所有节点都拿着同一根棒，往上面加东西。

这里用 TypedDict 定义状态的字段和类型，相当于规定了「接力棒里只能装什么东西」
"""
class MyState(TypedDict):
    # 状态里的第一个字段，字符串类型
    key_1: str
    # 状态里的第二个字段，字符串类型
    key_2: str
    # 状态里的第三个字段，字符串类型
    key_3: str


# ========== 3. 定义业务节点函数 ==========
"""
【节点是什么？】
节点就是工作流里的「执行步骤」，每个节点对应一个函数。
- 输入：当前的全局状态 state
- 输出：一个字典，里面是你要更新的状态字段，LangGraph 会自动把它合并到全局状态里

下面定义了 3 个节点，模拟工作流里的 3 个步骤
"""

def node_1(state: MyState) -> MyState:
    # 打印当前节点拿到的状态，方便我们看执行过程
    print('node_1状态为', state)
    # 返回要更新的内容：给 key_1 赋值 value_1，会自动合并到全局状态里
    return {"key_1": "value_1"}


def node_2(state: MyState) -> MyState:
    print('node_2状态为', state)
    # 这行是用来「模拟崩溃」的测试代码
    # 放开注释的话，执行到 node_2 就会主动报错，模拟程序崩了，用来测试断点恢复
    # raise Exception("模拟node_2节点报错")
    return {"key_2": "value_2"}


def node_3(state: MyState) -> MyState:
    print('node_3状态为', state)
    return {"key_3": "value_3"}


# ========== 4. 构建工作流图 ==========
def build_graph():
    # 1. 初始化一个「状态图」对象，指定它使用我们定义的 MyState 作为状态结构
    workflow = StateGraph(MyState)

    # 2. 往图里添加 3 个节点
    # 格式：add_node(节点名字, 对应的执行函数)
    workflow.add_node("node_1", node_1)
    workflow.add_node("node_2", node_2)
    workflow.add_node("node_3", node_3)

    # 3. 用「边」定义节点的执行顺序（箭头方向）
    # 起点 START 之后，先执行 node_1
    workflow.add_edge(START, "node_1")
    # node_1 执行完之后，执行 node_2
    workflow.add_edge("node_1", "node_2")
    # node_1 执行完之后，同时也执行 node_3
    # 【注意】这里 node_1 同时指向 node_2 和 node_3，是「并行分支」
    # 也就是 node_1 跑完后，node_2 和 node_3 会同时开始执行
    workflow.add_edge("node_1", "node_3")
    # node_2 执行完之后，走到终点 END
    workflow.add_edge("node_2", END)
    # node_3 执行完之后，走到终点 END
    workflow.add_edge("node_3", END)

    # 把搭建好的图返回出去
    return workflow


# ========== 5. 主函数：运行演示 ==========
def demo_langgraph():
    # --------------------------
    # 步骤1：准备 SQLite 数据库连接
    # --------------------------
    # 先创建一个文件夹 ./sqlite_data，用来放数据库文件
    # exist_ok=True：如果文件夹已经存在，也不会报错
    os.makedirs("./sqlite_data", exist_ok=True)

    # 创建 SQLite 数据库连接对象
    # database：数据库文件的保存路径，会自动生成 .db 文件
    # check_same_thread=False：SQLite 默认只允许创建它的线程使用它
    #   但 LangGraph 内部可能会用不同的线程操作数据库，所以关掉这个限制，避免报错
    conn = sqlite3.connect(
        database="./sqlite_data/langgraph_sqlite.db",
        check_same_thread=False
    )

    # --------------------------
    # 步骤2：创建检查点保存器（存档器）
    # --------------------------
    # 把数据库连接传给 SqliteSaver，生成一个 checkpointer 实例
    # 之后图运行的每一步状态，都会通过这个对象存到 SQLite 里
    # 【安装提示】这个功能需要单独装包：pip install langgraph-checkpoint-sqlite
    checkpointer = SqliteSaver(conn)

    # --------------------------
    # 步骤3：构建并编译图
    # --------------------------
    # 调用上面的函数，拿到搭建好的工作流图
    graph = build_graph()

    # 编译图，同时把 checkpointer 传进去
    # 【关键】只有编译时传入了 checkpointer，图才会自动保存状态、支持断点恢复
    # 编译之后的 app 就是可以直接运行的工作流实例
    app = graph.compile(checkpointer=checkpointer)

    # --------------------------
    # 步骤4：定义运行配置
    # --------------------------
    # config 里最核心的就是 thread_id
    # 【thread_id 是什么？】
    # 相当于「存档的编号」：
    # - 同一个 thread_id 对应同一份状态存档
    # - 不同的任务/会话用不同的 thread_id，就不会互相干扰
    # 恢复断点的时候，必须用和上次一样的 thread_id，才能找到对应的存档
    config = {"configurable": {"thread_id": "a1"}}

    # --------------------------
    # 步骤5：第一次运行（正常执行 + 自动存档）
    # --------------------------
    # invoke 就是启动图执行
    # 第一个参数 {}：初始状态，这里传空字典，从空状态开始跑
    # 第二个参数 config：传入配置，指定用哪个 thread_id 存档
    # 执行过程中，每跑完一个节点，都会自动把最新状态存到数据库里
    result = app.invoke({}, config=config)

    # --------------------------
    # 步骤6：断点恢复（从存档处继续跑）
    # --------------------------
    # 【使用方法】注释掉上面的 invoke，放开下面这行
    # 第一个参数传 None：代表「不传入新的初始状态，从数据库里读上次的存档继续跑」
    # 场景模拟：
    # 1. 先放开 node_2 里的报错代码，运行一次，程序会在 node_2 崩溃
    # 2. 注释掉报错代码，再注释掉上面的正常 invoke，放开下面这行
    # 3. 程序会从 node_2 开始继续执行，不会重新跑 node_1，这就是断点恢复
    # result = app.invoke(None, config=config)

    # --------------------------
    # 步骤7：打印最终结果
    # --------------------------
    print(result)

    # 额外工具：打印整个图的 ASCII 结构图，方便直观查看流程
    # app.get_graph().print_ascii()


# ========== 程序入口 ==========
# 当直接运行这个 py 文件时，执行 demo_langgraph 函数
if __name__ == "__main__":
    demo_langgraph()
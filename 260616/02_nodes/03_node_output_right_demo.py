# 04_nodes/03_node_output_right_demo.py
from typing import TypedDict  # 定义图全局状态结构

# 导入LangGraph内置常量与图构建工具
from langgraph.constants import START, END  # START图起点 / END图终点
from langgraph.graph import StateGraph     # 状态图核心类

# -------------------------- 1. 定义全局共享状态 --------------------------
# TypedDict 约束整张图所有节点共用的数据字段
class MyState(TypedDict):
    query: str        # 用户原始提问（初始化传入）
    file_result: str  # 本地文件检索结果
    web_result: str   # 网络搜索结果
    final_answer: str # 汇总后的最终回答

# -------------------------- 2. 网络搜索节点（标准写法） --------------------------
def query_web(state: MyState) -> dict:
    """
    模拟联网搜索工具节点
    ✅ LangGraph规范：仅返回当前节点新增/修改的字段字典，不返回完整state
    框架会自动把返回的字典合并到全局State，不会覆盖其他字段
    """
    # 从全局状态读取用户问题
    query = state['query']
    # 只返回当前节点负责更新的web_result字段
    return {'web_result': f'{query}的网络搜索结果'}

# -------------------------- 3. 文件检索节点（标准写法） --------------------------
def query_file(state: MyState) -> dict:
    """
    模拟本地知识库文件检索节点
    和query_web为并行分支，两个节点同时执行
    """
    query = state['query']
    # 仅返回当前节点修改的file_result
    return {'file_result': f'{query}的文件搜索结果'}

# -------------------------- 4. 汇总生成答案节点 --------------------------
def answer(state: MyState) -> dict:
    """
    聚合节点：必须等待web、file两个并行节点全部执行完毕才会触发
    读取两份检索结果，整合生成最终回复
    """
    # 获取前面并行节点产出的数据
    web_result = state['web_result']
    file_result = state['file_result']
    # 拼接最终回答文本
    final_answer = f'LLM基于 {web_result}，{file_result} 的最终结果'
    # 只返回当前节点更新的final_answer字段
    return {'final_answer': final_answer}

# -------------------------- 5. 搭建并编译流程图 --------------------------
def build_graph():
    # 实例化状态图，绑定我们定义的状态MyState
    graph = StateGraph(MyState)

    # 将函数注册为图内节点，函数名自动作为节点标识
    graph.add_node(answer)
    graph.add_node(query_web)
    graph.add_node(query_file)

    # 设置流向边：起点START同时指向两个检索节点 → 并行并发执行
    graph.add_edge(START, 'query_web')
    graph.add_edge(START, 'query_file')

    # 两条并行分支全部流向汇总节点answer
    # LangGraph多入边机制：所有上游节点完成后才执行下游节点
    graph.add_edge('query_web', 'answer')
    graph.add_edge('query_file', 'answer')

    # 汇总完成后走到END，流程结束
    graph.add_edge('answer', END)

    # 编译图，生成可调用运行的应用实例
    return graph.compile()

# -------------------------- 6. 程序入口，执行图流程 --------------------------
if __name__ == '__main__':
    # 构建流程图实例
    app = build_graph()
    # 初始化状态，仅传入必填初始参数query
    init_state = {"query": "什么是Langgraph"}
    # 启动图运行，等待所有节点执行完成，返回完整最终状态
    final_state = app.invoke(init_state)
    # 打印最终生成的回答
    print(final_state['final_answer'])

"""
# 核心知识点区分（对比错误demo）
1. 规范返回规则
   错误：return 01_state 把完整状态返回，并发场景易出现数据覆盖、冗余
   正确：return {"字段名": 值} 只输出当前节点变更内容，框架自动合并状态

2. 并行执行逻辑
   START同时分发任务给query_web、query_file，两个节点并发运行；
   answer有两个上游依赖，需两个检索全部结束才执行聚合。

3. 状态合并原理
   LangGraph采用增量合并策略，每个节点返回的小字典只会更新对应key，
   其他未修改字段保留原值，不会丢失数据，多线程并行更安全。

# 程序输出结果
LLM基于 什么是Langgraph的网络搜索结果，什么是Langgraph的文件搜索结果 的最终结果
"""
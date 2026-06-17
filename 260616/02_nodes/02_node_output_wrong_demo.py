# 04_nodes/02_node_output_wrong_demo.py

from typing import TypedDict  # 用于定义图全局状态的数据结构

# 导入LangGraph核心常量与图构建工具
from langgraph.constants import START, END  # START：图入口节点；END：图结束节点
from langgraph.graph import StateGraph  # 状态图核心构建类

# ====================== 1. 定义全局状态 MyState ======================
# TypedDict：规定整张图运行过程中所有节点共享的数据字段
# 整张图的所有节点共用这一份状态，节点之间靠这个state传数据
class MyState(TypedDict):
    # 用户输入的原始提问，初始化时传入
    query: str
    # 文件检索节点输出的结果
    file_result: str
    # 网络搜索节点输出的结果
    web_result: str
    # 汇总后生成的最终回答
    final_answer: str

# ====================== 2. 网络搜索节点函数 ======================
def query_web(state: MyState) -> dict:
    """
    功能模拟：联网搜索工具节点
    【重点错误演示】：直接把完整state返回，这是不规范写法
    LangGraph节点规范：只返回「当前节点新增/修改的字段字典」，不要返回完整state
    """
    # 从全局状态中取出用户原始问题
    query = state['query']
    # 在全局state里直接修改web_result字段
    state['web_result'] = f'{query}的网络搜索结果'
    # 错误写法：直接返回完整的state字典
    # 问题：LangGraph会做状态合并，返回全量state会带来冗余、并发场景容易出现覆盖bug
    return state

# ====================== 3. 文件检索节点函数 ======================
def query_file(state: MyState) -> dict:
    """
    功能模拟：本地文件知识库检索节点
    和query_web是并行节点，会同时执行
    同样存在返回完整state的错误写法
    """
    # 获取用户查询问题
    query = state['query']
    # 给状态的文件结果字段赋值
    state['file_result'] = f'{query}的文件搜索结果'
    # 错误：返回完整全局状态
    return state

# ====================== 4. 汇总回答节点函数 ======================
def answer(state: MyState) -> dict:
    """
    汇总节点：必须等网络、文件两个并行节点全部执行完才会运行
    读取两个检索结果，拼接生成最终答案存入state
    """
    # 读取并行节点产出的两份检索数据
    web_result = state['web_result']
    file_result = state['file_result']
    # 拼接生成最终回答文本
    final_answer = f'LLM基于{web_result}，{file_result} 的最终结果'
    # 将最终答案写入全局状态
    state['final_answer'] = final_answer
    # 同样错误写法，返回完整state
    return state

# ====================== 5. 搭建LangGraph流程图 ======================
def build_graph():
    # 初始化状态图，绑定我们前面定义好的状态结构MyState
    graph = StateGraph(MyState)

    # 把三个业务函数注册为图中的独立节点，函数名自动作为节点名称
    graph.add_node(answer)       # 汇总回答节点
    graph.add_node(query_web)    # 网络搜索节点
    graph.add_node(query_file)   # 文件检索节点

    # 设置边：定义节点执行流向
    # START是图的起点，同时指向两个节点 → 并行执行（并发分支）
    graph.add_edge(START, 'query_web')
    graph.add_edge(START, 'query_file')

    # 两条并行分支都指向answer汇总节点
    # LangGraph默认等待所有前置节点全部完成，才会执行下游answer节点
    graph.add_edge('query_web', 'answer')
    graph.add_edge('query_file', 'answer')

    # 汇总节点执行完成后，流向END结束节点，整张图运行终止
    graph.add_edge('answer', END)

    # 编译图：生成可调用、可运行的应用实例app
    return graph.compile()

# ====================== 6. 程序入口，运行流程图 ======================
if __name__ == '__main__':
    # 调用构建函数，拿到编译完成的图应用
    app = build_graph()

    # 初始化状态：只需要传入初始必填字段query，其他字段运行中节点自动填充
    init_state = {"query": "什么是Langgraph"}

    # invoke启动图执行，传入初始状态，等待全部节点跑完返回最终完整状态
    final_state = app.invoke(init_state)

    # 从最终状态字典取出生成好的最终答案并打印
    print(final_state['final_answer'])

"""
补充小白必看知识点：
1. 代码核心错误点
   所有节点return state是错误示范，标准写法只返回修改的字段：
   正确示例：
   def query_web(01_state):
       query = 01_state["query"]
       web_res = f"{query}的网络搜索结果"
       # 只返回变更字段，LangGraph自动合并到全局state
       return {"web_result": web_res}

2. 并行执行逻辑
   START同时指向query_web、query_file，两个节点并发运行；
   answer节点有两个上游依赖，必须两个节点全部执行完毕才会运行。

3. State合并机制
   LangGraph每次节点返回字典，会自动合并进全局状态，不会覆盖未修改字段；
   如果直接return完整state，多并发场景下容易出现状态互相覆盖丢失数据。

4. 运行输出结果
   LLM基于什么是Langgraph的网络搜索结果，什么是Langgraph的文件搜索结果 的最终结果
"""
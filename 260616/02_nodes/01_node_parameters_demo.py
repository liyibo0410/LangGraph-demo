# 04_nodes/01_node_parameters_demo.py
"""
客服系统完整示例
核心学习目标：弄懂 LangGraph 节点里两大核心参数 01_state、config 的区别和用法
1. 01_state：保存单次对话流程里的业务数据（用户问题、AI回复、操作日志）
2. config：保存全局不变的工具、用户身份信息（大模型客户端、数据库、用户ID）
3. 官方标准节点函数只能有 0/1/2 个入参：(01_state) 或者 (01_state, config)，不能自己加 runtime/context
"""

# 导入基础类型注解，List代表列表，TypedDict用来规范状态字典格式
from typing import TypedDict, List
# RunnableConfig：专门存放全局配置、工具实例的标准对象
from langchain_core.runnables import RunnableConfig
# LangGraph绘图核心类：StateGraph图、START起点、END终点
from langgraph.graph import StateGraph, START, END


# ====================== 模拟工具类1：假装是调用大模型的客户端 ======================
class MockLLM:
    """模拟大模型，只实现最简单的invoke方法，输入提示词，返回AI回答"""
    def invoke(self, prompt: str):
        # 把收到的prompt包装成回答返回
        return f"AI生成答案：'{prompt}'"


# ====================== 模拟工具类2：假装是操作数据库的客户端 ======================
class MockDatabase:
    """模拟用户数据库，根据用户id判断是VIP还是普通用户"""
    def get_user_info(self, user_id: str):
        # id里带vip就是vip用户，否则普通用户
        user_role = "vip" if "vip" in user_id else "standard"
        return {"id": user_id, "role": user_role}


# ====================== 定义流程图的状态 State（固定格式用TypedDict） ======================
class CustomerSupportState(TypedDict):
    """
    状态说明：所有单次流程内会变化的数据全部放这里
    每次调用一次graph.invoke，就会生成一份全新的state，流程结束自动销毁
    """
    query: str        # 用户输入的提问，每次对话都不一样
    response: str     # AI最终给用户的回复
    log: List[str]    # 本次处理的操作日志，记录过程


# ====================== 定义核心节点函数（处理客服逻辑） ======================
def node_customer_service(
    state: CustomerSupportState,  # 第一个固定参数：本次流程的临时业务数据
    config: RunnableConfig        # 第二个可选参数：全局配置、工具、用户身份
) -> dict:
    """
    客服业务处理节点
    输入：01_state（本次对话数据） + config（全局工具/用户信息）
    返回：字典，用来更新state里的字段（不需要全量返回，只写要修改的字段）
    """
    # -------------------------- 第一部分：从 01_state 拿本次用户提问 --------------------------
    # state里存的是这一轮用户刚发的问题，只在这次对话生效
    user_query = state["query"]
    print(f"【来自state】本次用户提问：{user_query}")

    # -------------------------- 第二部分：从 config 拿全局配置和工具 --------------------------
    # configurable是config里专门放自定义内容的字典，get防止不存在时报错，空字典兜底
    configurable = config.get("configurable", {})
    # 取出用户id，找不到就默认guest游客
    user_id = configurable.get("user_id", "guest")
    # 取出提前注入好的大模型工具实例
    llm_client = configurable.get("llm_client")
    # 取出提前注入好的数据库工具实例
    db_client = configurable.get("db_client")
    print(f"【来自config】当前操作用户ID：{user_id}")

    # 校验工具是否正常注入，如果缺失直接返回错误信息更新到state
    if not llm_client or not db_client:
        return {
            "response": "系统错误: LLM大模型或数据库客户端未正常加载",
            "log": ["运行报错：缺少全局工具依赖"]
        }

    # -------------------------- 第三部分：调用数据库查询用户身份 --------------------------
    user_info = db_client.get_user_info(user_id)
    user_role = user_info.get("role")
    print(f"【数据库查询结果】该用户身份：{user_role}")

    # -------------------------- 第四部分：根据身份组装提示词，调用AI --------------------------
    # 区分VIP/普通用户生成不同prompt（演示config里用户信息的作用）
    prompt = f"用户身份({user_role})，提问内容：{user_query}"
    # 调用模拟大模型生成回答
    llm_response = llm_client.invoke(prompt)

    # -------------------------- 第五部分：返回数据更新state --------------------------
    # 这里只返回需要修改的response和log，不需要返回query，框架会自动合并到原state
    return {
        "response": llm_response,
        "log": [f"处理完成：用户{user_id}咨询「{user_query}」"]
    }


# ====================== 封装流程图构建函数 ======================
def build_graph():
    """搭建客服完整流程图，最后返回编译好的可运行图对象"""
    # 1. 创建状态图，绑定我们定义好的CustomerSupportState状态规则
    workflow = StateGraph(CustomerSupportState)

    # 2. 向图里添加节点：给节点起名"customer_service"，绑定上面写好的处理函数
    workflow.add_node("customer_service", node_customer_service)

    # 3. 设置流程走向：START程序起点 → 客服处理节点
    workflow.add_edge(START, "customer_service")
    # 4. 设置流程走向：客服处理节点 → END程序终点
    workflow.add_edge("customer_service", END)

    # 编译图，返回可调用运行的app实例
    return workflow.compile()


# ====================== 程序入口（运行代码从这里开始执行） ======================
if __name__ == "__main__":
    # 1. 先构建、编译流程图，得到可执行对象app
    app = build_graph()

    # 2. 初始化本次对话的初始state（单次流程的临时数据）
    initial_state = {
        "query": "如何升级会员？",  # 用户本次的问题
        "log": []                   # 日志初始为空列表
    }

    # 3. 初始化全局config配置（所有会话通用的工具、用户信息放这里）
    run_config = {
        "configurable": {
            "user_id": "vip_user_999",   # 当前登录用户id
            "llm_client": MockLLM(),    # 全局唯一的大模型工具
            "db_client": MockDatabase() # 全局唯一的数据库工具
        }
    }

    print("===== 流程图开始执行 =====")
    # 运行流程图：传入初始状态state，和全局配置config
    result = app.invoke(input=initial_state, config=run_config)

    # 打印执行完成后的完整state结果
    print("\n===== 流程执行完毕，最终全部状态数据 =====")
    print(result)
# 03_state/13_langchain_checkpointer_demo.py
"""
功能演示：基于LangChain封装的create_agent + Checkpointer内存持久化
核心效果：同一个thread_id会话，多轮对话自动记住上下文，不会丢失历史聊天记录
"""
# 导入系统工具os（配置文件里读取环境变量会用到，这里主文件暂时不用）
import os

from anyio.lowlevel import checkpoint
# 从langchain的agent模块导入创建智能体的函数
from langchain.agents import create_agent
# 导入通用大模型初始化工具init_chat_model，兼容openai格式所有模型（硅基/通义/DeepSeek都能用）
from langchain.chat_models import init_chat_model
# 导入自定义工具装饰器 @tool，用来给大模型提供可调用的工具函数
from langchain.tools import tool
# 导入内存检查点存储器，用来临时保存每一轮对话的状态、上下文
from langgraph.checkpoint.memory import InMemorySaver
# 导入我们自己写的模型配置文件，读取模型名称、密钥、接口地址等参数
from lm_config import lm_config

# ====================== 第一步：初始化大模型客户端 ======================
# init_chat_model 统一初始化各类兼容OpenAI接口的大模型
llm_client = init_chat_model(
    # 模型名称，从lm_config配置文件读取 deepseek-ai/DeepSeek-V4-Flash
    model=lm_config.llm_model,
    # 接口兼容模式固定填openai，硅基流动、阿里云百炼都是openai兼容接口
    model_provider=lm_config.model_provider,
    # 硅基流动接口地址
    base_url=lm_config.base_url,
    # 你的硅基平台密钥
    api_key=lm_config.api_key
)

# =================== 第二步：创建内存检查点（状态存储器） ==================
# InMemorySaver = 内存存储，程序关闭/重启后所有对话记录全部消失，仅本地测试使用
checkpointer = InMemorySaver()

# =================== 第三步：定义大模型可以调用的工具函数 ==================
# @tool 装饰器：把普通Python函数包装成大模型能识别、主动调用的工具
@tool
def weather_tool(city: str, date: str) -> str:
    """
    查询指定城市、指定日期的天气
    Args:
        city: 需要查询天气的城市名字，字符串
        date: 查询日期，格式必须是 YYYY-MM-DD
    """
    # 模拟天气查询返回结果
    return f'{city}在{date}的天气是晴朗的，适合出门'

# =================== 第四步：构建带记忆存储的Agent智能体 ===================
agent = create_agent(
    # 绑定我们初始化好的DeepSeek大模型
    model=llm_client,
    # 给agent绑定可用工具，这里只有天气查询工具
    tools=[weather_tool],
    # 关键参数：传入checkpointer，开启会话状态持久化、上下文记忆功能
    checkpointer=checkpointer,
)

# ================ 第五步：会话配置，thread_id是会话唯一标识 ================
# config固定格式：configurable里面的thread_id用来区分不同用户/不同聊天窗口
# 相同thread_id = 同一个聊天会话，自动加载历史对话；不同id完全隔离互不干扰
session_config = {"configurable": {"thread_id": "user_session1"}}

# ========================= 第六步：第一次调用对话 ========================
# input={"messages": 给用户提问内容
# config=会话配置，指定当前对话属于user_session1这个会话
user_res1 = agent.invoke(
     input={"messages": "北京2026-06-16天气怎么样"},
     config=session_config
)
# 打印第一轮大模型最终回复，messages列表最后一条就是AI回答
print('=====第一次对话输出=====')
print(user_res1['messages'][-1].content)

# =============== 第七步：同一会话第二次追问（自动读取上下文） ================
# 不用重复写北京、日期！checkpointer保存了上一轮全部对话历史，AI能看懂上下文
user_res2 = agent.invoke(
    input={"messages": "那今天适合出去玩吗？"},
    config=session_config
)
print('\n=====第二次对话输出（复用历史上下文）=====')
print(user_res2['messages'][-1].content)

# ===================== 拓展：全新会话，无历史记忆 =====================
# print("\n=====更换thread_id，全新会话====")
# user_res3 = agent.invoke(
#     input={"messages": "今天上海天气"},
#     config=new_session_config
# )
# print(user_res3["messages"][-1].content)
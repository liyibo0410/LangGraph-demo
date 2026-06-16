# 第一步：必须加载环境变量
from dotenv import load_dotenv

load_dotenv()

import os
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

store = {}


# 用于存取数据的函数
def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


# 提示词模版
prompt = ChatPromptTemplate.from_messages([
    ('system', '你是一个AI助手'),
    MessagesPlaceholder(variable_name='history'),
    ('human', '{input}')
])

# ✅ 修复：填入硅基流动密钥
llm = ChatOpenAI(
    model="Qwen/Qwen2.5-7B-Instruct",  # 稳定可用
    api_key=os.getenv("SILICON_API_KEY"),
    base_url=os.getenv("SILICON_BASE_URL"),
    temperature=0.7
)

# 基础链
chain = prompt | llm

# 包装记忆组件
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key='input',
    history_messages_key='history',
)

# 多轮对话测试
if __name__ == "__main__":
    print("🚀 第一轮对话：")
    res1 = chain_with_history.invoke(
        {'input': '我叫牛依豪'},
        config={'configurable': {'session_id': 'niuyihao'}}
    )
    print(res1.content)

    print("-----------------------------")

    print("🔁 第二轮对话（带记忆）：")
    res2 = chain_with_history.invoke(
        {'input': '我叫什么'},
        config={'configurable': {'session_id': 'niuyihao'}}
    )
    print(res2.content)


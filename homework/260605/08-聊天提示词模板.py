from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", '你是一个专业的{role}'),
    ('human', "请回答关于{topic}的问题"),
    ('ai', "好的,我会尽力回答"),
    ('human', '{question}')
])

msg = chat_prompt.invoke({
    'role':'情感专家',
    'topic':'情感',
    "question":"我好难受"
})

llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V4-Flash"
)
print(llm.invoke(msg).content)


# from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
# from langchain_core.prompts import ChatPromptTemplate
#
# chat_prompt = ChatPromptTemplate.from_messages([
#     SystemMessage(content="你是一个有帮助的AI助手"),    # 固定内容用Message对象
#     HumanMessage(content="你好！"),                     # 固定内容
#     AIMessage(content="你好！有什么可以帮助你的？"),      # 固定内容
#     ("human", "请介绍{topic}")                          # 含变量的用元组形式
# ])
#
# messages = chat_prompt.invoke({"topic": "LangChain"})
# print(messages)
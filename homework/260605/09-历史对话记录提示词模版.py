from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

# prompt = ChatPromptTemplate.from_messages([
#     ("system", "你一个温情的AI助手"),
#     MessagesPlaceholder(variable_name="history"),  # 对话历史插槽
#     ('human', "{input}")
# ])
# 等价
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是AI助手"),
    ("placeholder", "{history}"),    # 等同于MessagesPlaceholder
    ("human", "{input}")
])

msg = prompt.invoke({
    'history':[
        HumanMessage(content='什么是爱?'),
        AIMessage(content='爱是不被定义的')
    ],
    "input":"它有什么特点"
})

llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V4-Pro",
    temperature=1.0
)
print(llm.invoke(msg).content)

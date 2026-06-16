from langchain_core.messages import HumanMessage,SystemMessage,AIMessage
# 系统 用户 AI 工具
from langchain_openai import ChatOpenAI

# 模拟多轮对话
# 对话历史——模拟多轮对话
# conversation = [
#     SystemMessage(content="你是一个情感专家"),
#     HumanMessage(content="你好，我叫张三,我好难受"),
#     AIMessage(content="具体是什么问题呢？"),
#     HumanMessage(content="心里难受？"),
# ]
# res = llm.invoke(conversation)


llm = ChatOpenAI(model="deepseek-ai/DeepSeek-V4-Flash", )

# # 元组方式：(角色, 内容)
# tuple_messages = [
#     ("system", "你是一个专业的Python编程助手"),
#     ("user", "什么是装饰器？")
# ]
#
# # 字典方式：{"role": 角色, "content": 内容}
# dict_messages = [
#     {"role": "system", "content": "你是一个专业的Python编程助手"},
#     {"role": "user", "content": "什么是装饰器？"}
# ]
# response = llm.invoke([
#     SystemMessage(content="你是一个情感专家"),
#     HumanMessage(content="我好难受？")
# ])
# print(response.content)


# 假设这是从配置文件读取的
prompt_template = [
    {"role": "system", "content": "你是一个{role}"},
    {"role": "user",   "content": "请解释{topic}"}
]

# 动态填充
messages = [
    {
        "role": t["role"],
        "content": t["content"].format(
            role="翻译助手",
            topic="机器翻译",
        ),
    }
    for t in prompt_template
]
print(llm.invoke(messages).content)


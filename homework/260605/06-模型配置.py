from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")
print(llm.profile)# 能够看到模型的能力 与配置 限制信息
# {
#     'max_input_tokens': 128000,
#     'image_inputs': True,
#     'tool_calling': True,
#     'structured_output': True,
#     ...
# }
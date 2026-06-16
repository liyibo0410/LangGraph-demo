# from langchain_core.prompts import PromptTemplate
# from langchain_openai import ChatOpenAI
#
# prompt = PromptTemplate.from_template("讲一个关于{topic}的{type}故事")
# prompt2 = prompt.partial(type='爱情的')  # 预定义
#
# test = prompt2.invoke({'topic':'人工智能'})
#
#
#
# print(test)
# llm = ChatOpenAI(
#     model="deepseek-ai/DeepSeek-V4-Flash"
# )
# res = llm.invoke(test)
# print(res.content)
# 方式一：调用partial方法固定部分变量
# from langchain_core.prompts import PromptTemplate
#
# prompt = PromptTemplate.from_template(
#     "讲一个关于{topic}的{adjective}故事"
# )
# fixed_prompt = prompt.partial(adjective="有趣的")
# print(fixed_prompt.invoke({"topic": "编程"}))
# # 输出: text='讲一个关于编程的有趣的故事'
#
# # 方式二：创建时直接指定partial_variables
# prompt = PromptTemplate(
#     template="请解释{concept}，使用{style}风格",
#     input_variables=["concept"],
#     partial_variables={"style": "简单易懂"}
# )
# print(prompt.invoke({"concept": "递归"}))
# # 输出: text='请解释递归，使用简单易懂风格'
from langchain_core.prompts import PromptTemplate

# 方式一：调用partial方法固定部分变量
prompt = PromptTemplate.from_template(
    "讲一个关于{topic}的{adjective}故事"
)
fixed_prompt = prompt.partial(adjective="有趣的")
print(fixed_prompt.invoke({"topic": "编程",'adjective':"无趣的"}))
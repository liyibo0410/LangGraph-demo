# 顺序
from langchain_core.runnables import  RunnableLambda
#
# # RunnableSequence 顺序流
# sequenece_chain = RunnableSequence(
#     first=RunnableLambda(lambda x: x.upper()),
#     middle=[RunnableLambda(lambda x: f"HELLO {x} !"),RunnableLambda(lambda x: f"哈哈 {x}")],
#     last=RunnableLambda(lambda x: f"最终输出: {x}")
# )
# res = sequenece_chain.invoke('world')
# print(res)
# 推荐
chain = (
        RunnableLambda(lambda x: x.upper()) |
        RunnableLambda(lambda x: f"HELLO {x}")|
        RunnableLambda(lambda x: f"最终输出 {x}")
         )
res = chain.invoke('world')
print(res)


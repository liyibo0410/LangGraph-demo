from langchain_core.runnables import RunnableSequence, RunnableParallel, RunnableLambda

# ======================
# 1. 并行任务（同时执行多个处理）
# ======================
p_chain = RunnableParallel({
    '长度': RunnableLambda(lambda x: len(x)),          # 计算字符串长度
    '大写': RunnableLambda(lambda x: x.upper()),      # 转大写
    '单词数': RunnableLambda(lambda x: len(x.split())), # 统计单词数量
    '反转': RunnableLambda(lambda x: x[::-1]),        # 字符串反转
})

# ======================
# 2. 顺序任务（一个接一个执行）
# ======================
s_chain = RunnableSequence(
    RunnableLambda(lambda x: x.upper()),  # 第一步：转大写
    RunnableLambda(lambda x: x + "!!!")   # 第二步：加感叹号
)

# ======================
# 测试运行
# ======================
if __name__ == "__main__":
    print("===== 并行执行结果 =====")
    res_parallel = p_chain.invoke("hello world LangChain")
    print(res_parallel)

    print("\n===== 顺序执行结果 =====")
    res_sequence = s_chain.invoke("hello world")
    print(res_sequence)
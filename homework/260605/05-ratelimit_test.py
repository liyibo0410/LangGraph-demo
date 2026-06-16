from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_openai import ChatOpenAI
import time
# 限流组件
a = InMemoryRateLimiter(
    requests_per_second=0.1,# 意味着每秒钟生成0.1个令牌
    check_every_n_seconds=0.1# 每0.1秒 检查一下桶里面有没有令牌
)

llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V4-Flash",
    rate_limiter=a,# 限流
)
def test_rate_limit(n=3):
    print("开始时间：", time.strftime("%X"))
    last = time.time()
    for i in range(n):
        t0 = time.time()
        resp = llm.invoke(f"第 {i} 次调用，简单回一句话就行")
        t1 = time.time()
        print(
            f"调用 {i} 完成，耗时 {t1 - t0:.2f}s，"
            f"距上次调用结束间隔 {t1 - last:.2f}s"
        )
        last = t1

test_rate_limit(3)


import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

# 1. 定义提示词和解析器
prompt = ChatPromptTemplate.from_template("请用一句话夸奖一下：{target}")
parser = StrOutputParser()

# 2. 初始化基础大模型
# 提示：我们可以故意把 timeout 设得很短（比如 0.01 秒），来强行模拟“网络超时错误”
llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V4-Flash",
    temperature=0,
    base_url=os.getenv("SILICON_BASE_URL"),
    api_key=os.getenv("SILICON_API_KEY")
)

# 3. 核心：为 LLM 组件外挂“自动重试”安全外挂
# 如果第一次失败，它会在后台默默发起第二次、第三次，直到超过 3 次才彻底死心
llm_with_retry = llm.with_retry(
    stop_after_attempt=3  # 最大尝试次数（1次正常调用 + 2次重试）
)

# 4. 组装 LCEL 链（把带重试的模型放进去）
retry_chain = prompt | llm_with_retry | parser

# 5. 执行调用
if __name__ == "__main__":
    try:
        print("🚀 正在发起请求（如果网络抖动，后台会自动重试）...")

        result = retry_chain.invoke({"target": "正在努力学习 LangChain 的开发者"})

        print("\n✨ [调用成功] 最终大模型回复：")
        print(result)

    except Exception as e:
        # 如果后台默默尝试了 3 次全部失败，最后才会把错误抛到这里
        print("\n❌ [最终失败] 哪怕重试了 3 次，依然没救回来。错误原因：")
        print(e)
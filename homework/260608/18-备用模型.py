import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# 加载环境变量（你的密钥）
load_dotenv()

# ======================
# 1. 主力模型（故意写错，必报错，模拟崩溃）
# ======================
primary_llm = ChatOpenAI(
    model="xxxxxx",  # 不存在的模型，必报错
    api_key=os.getenv("SILICON_API_KEY"),
    base_url=os.getenv("SILICON_BASE_URL"),
)

# ======================
# 2. 备用模型（硅基流动 正常可用模型）
# ======================
llm1 = ChatOpenAI(
    model="Qwen/Qwen2.5-7B-Instruct",  # 硅基流动免费可用
    api_key=os.getenv("SILICON_API_KEY"),
    base_url=os.getenv("SILICON_BASE_URL"),
)

llm2 = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V3",  # 备用第二个
    api_key=os.getenv("SILICON_API_KEY"),
    base_url=os.getenv("SILICON_BASE_URL"),
)

# ======================
# 3. 绑定 fallback 自动回退
# ======================
llm_with_fallback = primary_llm.with_fallbacks([llm1, llm2])

# ======================
# 4. 组装链
# ======================
fallback_chain = (
    ChatPromptTemplate.from_template("请用一句话解释什么是【{concept}】")
    | llm_with_fallback
    | StrOutputParser()
)

# ======================
# 5. 运行测试
# ======================
if __name__ == "__main__":
    print("🚀 测试：主力模型挂掉 → 自动切备用模型")

    try:
        result = fallback_chain.invoke({"concept": "大模型回退机制"})
        print("\n✅ 调用成功！（备用模型自动救场）")
        print("回复内容：", result)

    except Exception as e:
        print("\n❌ 全部模型都失败了：", e)
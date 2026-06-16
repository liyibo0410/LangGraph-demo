# 加载环境变量，读取硅基流动密钥
from dotenv import load_dotenv
load_dotenv()
import os

from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 初始化硅基流动兼容OpenAI接口的模型
llm = init_chat_model(
    model="Qwen/Qwen2.5-7B-Instruct",
    model_provider="openai",
    api_key=os.getenv("SILICON_API_KEY"),
    base_url=os.getenv("SILICON_BASE_URL")
)

# 两个并行赏析链：分别分析含义、意境
paragraph_1_chain = (
    PromptTemplate.from_template("对这首诗做赏析，分析含义：{poem}")
    | llm | StrOutputParser()
)
paragraph_2_chain = (
    PromptTemplate.from_template("对这首诗做赏析，分析意境：{poem}")
    | llm | StrOutputParser()
)

# 汇总对比链
summary_chain = (
    PromptTemplate.from_template(
        "第一种赏析：{paragraph_1}\n\n第二种赏析：{paragraph_2}\n\n请比较哪个更好，说明理由"
    )
    | llm | StrOutputParser()
)

# LCEL并行语法：字典会并行执行内部两条链，收集结果再传入汇总链
full_chain = {
    "paragraph_1": paragraph_1_chain,
    "paragraph_2": paragraph_2_chain,
} | summary_chain

# 执行
if __name__ == "__main__":
    resp = full_chain.invoke({"poem": "菩提本无树，明镜亦非台，本来无一物，何处惹尘埃。"})
    print(resp)
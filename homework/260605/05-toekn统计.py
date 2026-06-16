from langchain_core.callbacks import get_usage_metadata_callback#收集大模型返回的 usage_metadata（即 Token 统计信息）
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V4-Flash"
)

with get_usage_metadata_callback() as cb:
    llm.invoke("你好")
    llm.invoke("再见")

    print(cb.usage_metadata)
    # {
    #     'input_tokens': 总输入token数,
    #     'output_tokens': 总输出token数,
    #     'total_tokens': 总token数
    # }
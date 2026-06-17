from langchain_openai import ChatOpenAI
# 重点：带上文件夹名260616
from lm_config import lm_config

# 实例化模型
llm = ChatOpenAI(
    model=lm_config.llm_model,
    temperature=lm_config.temperature,
    base_url=lm_config.base_url,
    api_key=lm_config.api_key
)

# 测试调用
if __name__ == "__main__":
    res = llm.invoke("你好")
    print(res.content)
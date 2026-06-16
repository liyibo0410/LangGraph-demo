# Langchain
# 第一种  DeepSeek
from langchain_openai import ChatOpenAI
import os
import dotenv

dotenv.load_dotenv()
# 0.x 兼容写法
# llm = ChatOpenAI(base_url=os.getenv("SILICONFLOW_BASE_URL"),
#                  api_key=os.getenv("SILICONFLOW_API_KEY"),
#                  model="Pro/moonshotai/Kimi-K2.6",
# temperature = 0.7,  # 随机性，0=确定性，1=有创意（默认因模型而异）
# max_tokens = 1000,  # 最大输出长度
# timeout = 60,  # 超时时间（秒）
# max_retries = 2,  # 失败重试次数
#
#                  )
# llm = ChatDeepSeek(base_url=os.getenv("DEEPSEEK_BASE_URL"),
#              api_key=os.getenv("DEEPSEEK_API_KEY"),
#              model="deepseek-v4-flash"
#              )
# response = llm.invoke("一句话介绍你自己")
# print(response.content)

# 兼容写法 OpenAI  Gemini Claude


# 第二种写法  init_chat_model
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os
load_dotenv()

# 一个函数搞定所有提供商，通过 model_provider 参数区分
llm_openai = init_chat_model(model="deepseek-ai/DeepSeek-V4-Pro",
                             model_provider="deepseek",
                             api_key=os.getenv("SILICONFLOW_API_KEY"),
                             base_url=os.getenv("SILICONFLOW_BASE_URL"))
llm_claude = init_chat_model(model="Pro/zai-org/GLM-5.1",
                             model_provider="openai",
                             api_key=os.getenv("SILICONFLOW_API_KEY"),
                             base_url=os.getenv("SILICONFLOW_BASE_URL"))
llm_gemini = init_chat_model(model="Qwen/Qwen3.6-35B-A3B",  # 文本模型
                             model_provider="openai",
                             api_key=os.getenv("SILICONFLOW_API_KEY"),
                             base_url=os.getenv("SILICONFLOW_BASE_URL"))

# 调用方式完全一致
for name, llm in [("模型1",llm_openai),("模型2",llm_claude),("模型3", llm_gemini)]:
    response = llm.invoke("用一句话介绍你自己")
    print(f"{name}: {response.content}")

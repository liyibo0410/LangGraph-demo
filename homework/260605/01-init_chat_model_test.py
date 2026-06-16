from langchain.chat_models import init_chat_model
from openai import base_url
import os
import dotenv

dotenv.load_dotenv()

llm = init_chat_model(api_key=os.getenv("SILICONFLOW_API_KEY"),
                      base_url=os.getenv("SILICONFLOW_BASE_URL"),
                      model_provider="openai",
                      temperature=0)

# 使用时候 再指定
res1 = llm.invoke("一句话介绍你自己",
                  config={"configurable":
                              {"model": "deepseek-ai/DeepSeek-V4-Flash"}
                          }
                  )
res2 = llm.invoke("一句话介绍你自己",
                  config={"configurable":
                              {"model": "deepseek-ai/DeepSeek-V4-Pro"}
                          }
                  )
res3 = llm.invoke("一句话介绍你自己",
                  config={"configurable":
                              {"model": "MiniMaxAI/MiniMax-M2.5"}
                          }
                  )
print(res1)
print(res2)
print(res3)

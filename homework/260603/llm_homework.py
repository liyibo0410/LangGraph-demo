# 导入依赖
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model
# 加载.env环境变量
load_dotenv()

# ======================【方式1：ChatOpenAI实例化】======================
# 1.智谱清言-方式1
zhipu_llm1 = ChatOpenAI(
    model="glm-4-flash",
    api_key=os.getenv("ZHIPU_API_KEY"),
    base_url=os.getenv("ZHIPU_BASE_URL")
)
# 2.硅基流动-方式1
silicon_llm1 = ChatOpenAI(
    model="Qwen/Qwen2.5-7B-Instruct",
    api_key=os.getenv("SILICON_API_KEY"),
    base_url=os.getenv("SILICON_BASE_URL")
)

# ======================【方式2：init_chat_model工厂】======================
# 1.智谱清言-方式2
zhipu_llm2 = init_chat_model(
    model="glm-4-flash",
    model_provider="openai", # 智谱兼容openai协议，provider统一填openai
    api_key=os.getenv("ZHIPU_API_KEY"),
    base_url=os.getenv("ZHIPU_BASE_URL")
)
# 2.硅基流动-方式2
silicon_llm2 = init_chat_model(
    model="Qwen/Qwen2.5-7B-Instruct",
    model_provider="openai", # 硅基兼容openai协议，provider统一填openai
    api_key=os.getenv("SILICON_API_KEY"),
    base_url=os.getenv("SILICON_BASE_URL")
)

# ======================测试调用（验证4个llm对象全部可用）=====================
print("===智谱-ChatOpenAI方式===")
print(zhipu_llm1.invoke("你是哪家大模型？").content)

print("\n===智谱-init_chat_model方式===")
print(zhipu_llm2.invoke("你是哪家大模型？").content)

print("\n===硅基-ChatOpenAI方式===")
print(silicon_llm1.invoke("你是哪家大模型？").content)

print("\n===硅基-init_chat_model方式===")
print(silicon_llm2.invoke("你是哪家大模型？").content)
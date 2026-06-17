"""
硅基流动 DeepSeek V4 Flash 模型配置文件
仅存放配置参数，不初始化LLM
"""
from dataclasses import dataclass
import os
from dotenv import load_dotenv

# 读取.env环境变量
load_dotenv()

@dataclass
class LLMConfig:
    llm_model: str
    model_provider: str
    base_url: str
    api_key: str
    temperature: float

# 全局配置对象
lm_config = LLMConfig(
    llm_model="deepseek-ai/DeepSeek-V4-Flash",
    model_provider="openai",
    base_url=os.getenv("SILICON_BASE_URL"),
    api_key=os.getenv("SILICON_API_KEY"),
    temperature=0.0
)
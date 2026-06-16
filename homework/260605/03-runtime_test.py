from langchain_openai import ChatOpenAI
from langchain_core.callbacks import BaseCallbackHandler

# 1. 自定义一个回调处理器，拦截并打印运行信息
class MyDebugCallback(BaseCallbackHandler):
    def on_chat_model_start(self, serialized, prompts, **kwargs):
        print("\n" + "="*40)
        print(" [拦截到 LLM 启动请求]")
        print(f" Tags: {kwargs.get('tags')}")
        print(f" Metadata: {kwargs.get('metadata')}")

        print("="*40 + "\n")

llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V4-Flash"
)

# 2. 在调用时，将你的回调处理器传进去
response = llm.invoke(
    "讲一个短笑话",
    config={
        "tags": ["晴天", "操场"],
        "metadata": {"user_id": "我是张三"},
        "callbacks": [MyDebugCallback()]  # 关键：挂载你的回调
    }
)

print("最终返回的 response 依然只有大模型的内容：")
print(response.content)
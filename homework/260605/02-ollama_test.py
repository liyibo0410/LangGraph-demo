# qwen3:8b
from langchain_ollama import ChatOllama

llm = ChatOllama(model="qwen3:8b",base_url="http://localhost:11434")
res = llm.invoke("你好,介绍一下你自己")
print(res.content)
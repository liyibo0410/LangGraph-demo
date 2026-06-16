from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

embeddings = OpenAIEmbeddings(
    model="Qwen/Qwen3-Embedding-8B",
    api_key=os.getenv("SILICON_API_KEY"),
    base_url=os.getenv("SILICON_BASE_URL")
)

query = "什么是人工智能？"
docs = [
    "人工智能是计算机科学的一个分支",
    "机器学习是人工智能的子领域",
]

# 向量化
query_vector = embeddings.embed_query(query)
doc_vectors = embeddings.embed_documents(docs)

# 打印查询向量信息
print("=== 查询向量 ===")
print(f"查询文本: {query}")
print(f"向量维度: {len(query_vector)}")
print(f"向量前 5 维: {query_vector[:5]}")
print("=" * 40)

# 打印文档向量信息
print("=== 文档向量 ===")
for i, (text, vec) in enumerate(zip(docs, doc_vectors)):
    print(f"文档 {i}: {text}")
    print(f"向量维度: {len(vec)}")
    print(f"向量前 5 维: {vec[:5]}")
    print("-" * 40)
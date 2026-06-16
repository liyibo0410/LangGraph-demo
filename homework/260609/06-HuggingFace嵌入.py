def embedding_demo():
    from langchain_huggingface import HuggingFaceEmbeddings

    # 填写解压后存放的完整D盘路径
    embed_model = HuggingFaceEmbeddings(
        model_name=r'D:\software\ai_models\sentence_transformers_cache\bge-base-zh-v1.5',
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    # 单文本嵌入
    query = "你好，世界"
    query_result = embed_model.embed_query(query)
    print("单文本向量维度：", len(query_result))  # 输出768
    print("向量前10个值：", query_result[0:10])

    # 多文本批量嵌入
    docs = ["你好，世界", "你好，世界"]
    res = embed_model.embed_documents(docs)
    print("\n多文本返回类型：", type(res))  # list[list[float]]
    print("批量文本数量：", len(res))

if __name__ == "__main__":
    embedding_demo()

# 校验缓存路径
import os
from huggingface_hub.constants import HUGGINGFACE_HUB_CACHE
print("\nhuggingface hub缓存路径：", HUGGINGFACE_HUB_CACHE)
print("sentence-transformers缓存路径：", os.getenv("SENTENCE_TRANSFORMERS_HOME"))
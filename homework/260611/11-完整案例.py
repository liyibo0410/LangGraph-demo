import os
from pymilvus import MilvusClient, AnnSearchRequest, RRFRanker
from FlagEmbedding import BGEM3FlagModel

# ==========================================
# 1. 全局配置与客户端初始化
# ==========================================
COLLECTION_NAME = "demo_collection"
# 确保这里和上一节插入数据时使用的模型路径一致
MODEL_PATH = r"D:\software\ai_models\huggingface_cache\bge-m3"
MILVUS_URI = "http://localhost:19530"

print("-> 正在连接 Milvus 客户端...")
client = MilvusClient(uri=MILVUS_URI, token="")

print(f"-> 正在加载 BGE-M3 模型 (用于处理查询问题)...")
model = BGEM3FlagModel(MODEL_PATH)


# ==========================================
# 2. 辅助函数：将用户提问转换为向量
# ==========================================
def encode_query(query_text: str):
    """使用 BGE-M3 模型同时生成查询的稠密向量和稀疏向量"""
    vectors = model.encode(
        [query_text],
        return_dense=True,
        return_sparse=True
    )
    # 提取列表中的第一个（也是唯一一个）元素的向量
    dense_vec = vectors["dense_vecs"][0]
    sparse_vec = vectors["lexical_weights"][0]
    return dense_vec, sparse_vec


# ==========================================
# 3. 混合检索与重排序 (Hybrid Search + RRF)
# ==========================================
def hybrid_vector_search_example_rrf(query: str, limit: int = 3):
    print(f"\n[{' 混合检索测试 ':=^40}]")
    print(f"用户提问: {query}")

    # 1. 对查询语句进行向量化
    dense_vec, sparse_vec = encode_query(query)

    # 2. 构建稠密向量检索请求 (语义检索)
    # 注意：这里的 metric_type 必须与你创建索引时保持一致 (你之前代码里建的是 COSINE)
    dense_req = AnnSearchRequest(
        data=[dense_vec],
        anns_field="vector",
        param={"metric_type": "COSINE"},
        limit=limit,
    )

    # 3. 构建稀疏向量检索请求 (关键词检索)
    # 稀疏向量的度量方式通常使用 IP (内积)
    sparse_req = AnnSearchRequest(
        data=[sparse_vec],
        anns_field="sparse_vector",
        param={"metric_type": "IP"},
        limit=limit,
    )

    # 4. 执行混合检索，并使用 RRFRanker 重新排序
    results = client.hybrid_search(
        collection_name=COLLECTION_NAME,
        reqs=[dense_req, sparse_req],
        ranker=RRFRanker(k=60),  # k 决定了排名权重的衰减速度，一般设为 60
        limit=limit,
        output_fields=["id", "text", "metadata"],  # 告诉 Milvus 返回哪些原始字段
    )

    # 5. 打印结果
    print(f"\n--- 混合检索找到了 {len(results[0])} 条相关片段 ---")
    for i, hit in enumerate(results[0]):
        print(f"\nTop {i + 1} (匹配分数/RRF Score: {hit['distance']:.4f})")
        print(f"ID: {hit['id']}")
        print(f"来源文件: {hit['entity'].get('metadata', {}).get('source', '未知')}")
        print(f"文本内容: {hit['entity'].get('text', '')}")


# ==========================================
# 4. 标量检索 (精准过滤)
# ==========================================
def scalar_query_examples(keyword: str):
    print(f"\n[{' 标量检索测试 ':=^40}]")
    print(f"正在全文检索包含关键词 '{keyword}' 的片段...")

    # 对 text 字段进行模糊匹配 (类似 SQL 的 LIKE)
    like_res = client.query(
        collection_name=COLLECTION_NAME,
        filter=f'text like "%{keyword}%"',
        output_fields=["id", "text", "metadata"],
        limit=3,
    )

    print(f"\n--- 标量检索找到了 {len(like_res)} 条结果 ---")
    for i, res in enumerate(like_res):
        print(f"\n结果 {i + 1} (ID: {res['id']})")
        print(f"文本内容: {res['text']}")


# ==========================================
# 主运行入口
# ==========================================
if __name__ == "__main__":
    try:
        # 你可以根据你导入的 sample.docx 的实际内容，修改下面的提问词
        test_query = "孩子在校被同学打伤，学校未尽看管责任，打人学生家长 + 学校共同承担赔偿。？"

        # 执行混合检索测试
        hybrid_vector_search_example_rrf(query=test_query, limit=3)

        # 执行标量检索测试
        test_keyword = "模型"
        scalar_query_examples(keyword=test_keyword)

    except Exception as e:
        print(f"\n 检索过程中发生错误: {e}")
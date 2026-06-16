import os
from pymilvus import MilvusClient, DataType
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from FlagEmbedding import BGEM3FlagModel

# ==========================================
# 1. 定义 Schema (表结构)
# ==========================================
def build_schema():
    print("-> 正在构建 Schema...")
    return (
        MilvusClient.create_schema(auto_id=True)
        # 主键：自动生成ID
        .add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
        # 稠密向量：用于语义检索，维度需要与你的 BGE-M3 模型输出一致 (通常是 1024)
        .add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=1024)
        # 稀疏向量：用于关键词检索
        .add_field(field_name="sparse_vector", datatype=DataType.SPARSE_FLOAT_VECTOR)
        # 原始文本：存储Chunk内容，检索后返回给用户
        .add_field(field_name="text", datatype=DataType.VARCHAR, max_length=1500)
        # 元数据：存储来源、页码等信息，支持过滤
        .add_field(field_name="metadata", datatype=DataType.JSON)
    )

# ==========================================
# 2. 配置索引 (加速检索)
# ==========================================
def build_index():
    print("-> 正在配置索引参数...")
    index_params = MilvusClient.prepare_index_params()

    # 稠密向量：使用HNSW索引 + L2度量
    index_params.add_index(
        field_name="vector",
        index_type="HNSW",
        metric_type="COSINE",
    )

    # 稀疏向量：使用倒排索引 + IP度量
    index_params.add_index(
        field_name="sparse_vector",
        index_type="SPARSE_INVERTED_INDEX",
        metric_type="IP",
    )

    return index_params

# ==========================================
# 3. 创建客户端与 Collection (集合/表)
# ==========================================
def get_milvus_client():
    print("-> 正在连接 Milvus 客户端...")
    # 假设你的 Milvus 运行在本地默认端口
    return MilvusClient(uri="http://localhost:19530", token="")

def create_collection(client, collection_name):
    print(f"-> 准备创建 Collection: {collection_name}")

    # 为了演示方便，如果存在同名集合，先删除
    if client.has_collection(collection_name=collection_name):
        print(f"   发现已存在集合 {collection_name}，正在删除以重新创建...")
        client.drop_collection(collection_name=collection_name)

    # 创建集合，绑定前面定义的 Schema 和 索引参数
    print(f"   正在创建新集合...")
    client.create_collection(
        collection_name=collection_name,
        schema=build_schema(),
        index_params=build_index(),
    )
    print(f"   Collection {collection_name} 创建成功！")

# ==========================================
# 4. 数据处理与插入 (核心流程)
# ==========================================
def insert_data(client: MilvusClient, collection_name: str, doc_path: str, model_path: str):
    print(f"\n-> 开始处理数据并插入 Milvus...")

    # 检查文件是否存在
    if not os.path.exists(doc_path):
        print(f"   [错误] 找不到文档: {doc_path}。请确保文件存在。")
        return
    if not os.path.exists(model_path):
        print(f"   [警告] 找不到本地模型: {model_path}。如果是首次运行，它可能会自动下载。")

    print(f"   1. 加载文档: {doc_path}")
    doc_list = UnstructuredWordDocumentLoader(
        doc_path, mode="single"
    ).load()

    print(f"   2. 切分文档...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50, separators=["\n\n", "\n", "。"]
    )
    splitted_doc_list = text_splitter.split_documents(doc_list)
    print(f"      共切分为 {len(splitted_doc_list)} 个片段 (Chunks)。")

    print(f"   3. 加载 BGE-M3 模型并构建向量 (这可能需要一些时间)...")
    model = BGEM3FlagModel(model_path)
    all_vectors = model.encode(
        [doc.page_content for doc in splitted_doc_list],
        return_dense=True,
        return_sparse=True
    )

    print(f"   4. 准备数据列表...")
    insert_data_list = []
    for doc, dense_vector, sparse_vector in zip(
        splitted_doc_list,
        all_vectors["dense_vecs"],
        all_vectors['lexical_weights']
    ):
        insert_data_list.append({
            "vector": dense_vector,
            "sparse_vector": sparse_vector,
            "metadata": doc.metadata,
            "text": doc.page_content
        })

    print(f"   5. 正在将数据插入 {collection_name}...")
    res = client.insert(collection_name=collection_name, data=insert_data_list)
    print(f"-> 插入完成！Milvus 返回结果: {res}")


# ==========================================
# 主运行入口
# ==========================================
if __name__ == "__main__":
    COLLECTION_NAME = "demo_collection"
    # 如果没有示例 word 文档，请随便建一个测试文档。
    DOC_PATH = "sample.docx"
    # 如果你没有下载模型到本地，让它从 HuggingFace 自动下载
    MODEL_PATH = r"D:\software\ai_models\huggingface_cache\bge-m3"

    try:
        # 获取客户端连接
        milvus_client = get_milvus_client()

        # # 创建数据库集合
        create_collection(milvus_client, COLLECTION_NAME)

        # # 执行数据切分、向量化并插入
        insert_data(milvus_client, COLLECTION_NAME, DOC_PATH, MODEL_PATH)

        print("\n 全部流程执行完毕！可以打开 Attu 客户端查看插入的数据了。")

    except Exception as e:
        print(f"\n 运行过程中发生错误: {e}")
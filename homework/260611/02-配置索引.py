def build_index():
    from pymilvus import MilvusClient
    index_params = MilvusClient.prepare_index_params()

    # 稠密向量：使用HNSW索引 + L2度量
    index_params.add_index(
        field_name="vector",
        index_type="HNSW",
        metric_type="L2",
    )

    # 稀疏向量：使用倒排索引 + IP度量
    index_params.add_index(
        field_name="sparse_vector",
        index_type="SPARSE_INVERTED_INDEX",
        metric_type="IP",
    )

    return index_params
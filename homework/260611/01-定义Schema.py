def build_schema():
    from pymilvus import MilvusClient, DataType
    return (
        MilvusClient.create_schema(auto_id=True)
        # 主键：自动生成ID
        .add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
        # 稠密向量：用于语义检索，维度与嵌入模型一致
        .add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=1024)
        # 稀疏向量：用于关键词检索
        .add_field(field_name="sparse_vector", datatype=DataType.SPARSE_FLOAT_VECTOR)
        # 原始文本：存储Chunk内容，检索后返回给用户
        .add_field(field_name="text", datatype=DataType.VARCHAR, max_length=1500)
        # 元数据：存储来源、页码等信息，支持过滤
        .add_field(field_name="metadata", datatype=DataType.JSON)
    )



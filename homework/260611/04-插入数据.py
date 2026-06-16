from pymilvus import MilvusClient

def insert_data(client: MilvusClient, collection_name: str):
    from langchain_community.document_loaders import UnstructuredWordDocumentLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from FlagEmbedding import BGEM3FlagModel

    # 1、加载文件（已经改成你文件实际所在的路径）
    doc_list = UnstructuredWordDocumentLoader(
        "sample.docx", mode="single"
    ).load()
    print("✅ 文档加载成功")

    # 2、切分文件
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50, separators=["\n\n", "\n", "。"]
    )
    splitted_doc_list = text_splitter.split_documents(doc_list)
    print(f"✅ 文档切分完成，共 {len(splitted_doc_list)} 个片段")

    # 3、构建向量（已经改成你本地BGE-M3模型的路径）
    model = BGEM3FlagModel(r"D:\ai_models\huggingface_cache\bge-m3")
    all_vectors = model.encode(
        [doc.page_content for doc in splitted_doc_list],
        return_dense=True, return_sparse=True
    )
    print("✅ 双向量生成完成")

    # 4、组装Milvus入库数据
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

    # 5、批量插入向量库
    res = client.insert(collection_name=collection_name, data=insert_data_list)
    print(f"🎉 数据插入成功！共插入 {res['insert_count']} 条向量")
    return res
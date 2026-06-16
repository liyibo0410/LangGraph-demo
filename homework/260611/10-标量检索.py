def scalar_query_examples(client, keyword: str = "大模型"):
    # 对text字段进行模糊检索
    like_res = client.query(
        collection_name=COLLECTION_NAME,
        filter=f'text like "%{keyword}%"',
        output_fields=["id", "text"],
        limit=5,
    )

    # 对metadata的JSON字段进行检索
    json_res = client.query(
        collection_name=COLLECTION_NAME,
        filter='metadata["source"] like "%sample%"',
        output_fields=["id", "metadata"],
        limit=5,
    )

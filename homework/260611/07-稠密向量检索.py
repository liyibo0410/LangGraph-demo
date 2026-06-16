def dense_vector_search_example(client, query: str, limit: int = 5):
    model = get_bge_m3_model()
    dense_vec, _ = encode_query(model, query)

    results = client.search(
        collection_name=COLLECTION_NAME,
        data=[dense_vec],
        anns_field="vector",
        limit=limit,
        search_params={"metric_type": "COSINE"},
        output_fields=["id", "text", "metadata"]
    )
    return results[0]
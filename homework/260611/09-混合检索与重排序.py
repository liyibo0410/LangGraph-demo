def hybrid_vector_search_example_rrf(client, query: str, limit: int = 5):
    from pymilvus import AnnSearchRequest, RRFRanker

    model = get_bge_m3_model()
    dense_vec, sparse_vec = encode_query(model, query)

    dense_req = AnnSearchRequest(
        data=[dense_vec], anns_field="vector",
        param={"metric_type": "COSINE"}, limit=limit,
    )
    sparse_req = AnnSearchRequest(
        data=[sparse_vec], anns_field="sparse_vector",
        param={"metric_type": "IP"}, limit=limit,
    )

    results = client.hybrid_search(
        collection_name=COLLECTION_NAME,
        reqs=[dense_req, sparse_req],
        ranker=RRFRanker(k=60),
        limit=limit,
        output_fields=["id", "text", "metadata"],
    )
    return results[0]
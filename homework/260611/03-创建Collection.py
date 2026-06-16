def get_milvus_client():
    from pymilvus import MilvusClient
    return MilvusClient(uri="http://localhost:19530", token="")

def create_collection(client):
    collection_name = "demo_collection"
    client.drop_collection(collection_name=collection_name)
    if not client.has_collection(collection_name=collection_name):
        client.create_collection(
            collection_name=collection_name,
            schema=build_schema(),
            index_params=build_index(),
        )
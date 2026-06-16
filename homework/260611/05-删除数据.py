def delete_demo(client):
    res = client.delete(
        collection_name="demo_collection",
        # 通过ID删除，也可通过其他字段过滤
        filter="id in [463480757150366907, 463480757150366908]",
    )
    print(res)  # {'delete_count': 2}
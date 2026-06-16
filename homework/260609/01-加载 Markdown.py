# uv add markdown langchain-community "unstructured[md]"

import os

from langchain_community.document_loaders import UnstructuredMarkdownLoader


def markdown_loader_demo(file_path: str):
    """
    使用 UnstructuredMarkdownLoader 加载 Markdown 文件，
    并按 elements 模式打印切分后的内容。
    """

    # 1. 实例化UnstructuredMarkdownLoader文档加载器
    loader = UnstructuredMarkdownLoader(
        file_path,
        encoding="utf-8",
        mode="elements",  # elements：按标题、段落、列表等元素切分成多个文档对象 single:整个md的所有内容是一个文档对象
    )

    # 2. 文档加载器加载文档  # list[Document]
    docs = loader.load()
    print(f"加载后的文档数{len(docs)}")
    # 3. 打印加载后的文档信息
    for i, doc in enumerate(docs):
        print(f"=== Element {i} ===")
        print(doc.page_content)  # 文档内容
        print("metadata:", doc.metadata) # 文档的元数据
        print("============\n")


#  入口调用
markdown_loader_demo("./sample.md")
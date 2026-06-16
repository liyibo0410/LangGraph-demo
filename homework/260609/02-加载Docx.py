# 依赖安装（在终端中执行一次即可，而不是在 Python 里执行）
# uv add langchain-community "unstructured[docx]"

from pathlib import Path
from langchain_community.document_loaders import UnstructuredWordDocumentLoader


def word_loader_demo(file_path: str, start: int = 0, end: int = 20):
    """
    使用 UnstructuredWordDocumentLoader 加载 Word 文档（.docx），
    并打印指定区间的元素内容和元数据。

    :param file_path: .docx 文件路径
    :param start: 打印的起始索引
    :param end: 打印的结束索引（不含）
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在：{file_path.resolve()}")

    loader = UnstructuredWordDocumentLoader(
        file_path=str(file_path),
        mode="elements",  # 不会根据标题加载多个文档对象---根据行来加载文档对象
    )
    docs = loader.load()

    print(f"总共解析得到 {len(docs)} 个元素\n")

    end = min(end, len(docs))

    for i, doc in enumerate(docs[start:end], start=start):
        print(f"=== Element {i} ===")
        print(doc.page_content)
        print("metadata:", doc.metadata)
        print("============\n")

word_loader_demo("./sample.docx")
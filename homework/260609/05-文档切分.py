# pip install langchain-text-splitters
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredWordDocumentLoader

# 加载文档
docs = UnstructuredWordDocumentLoader(
    file_path="sample.docx",
    mode="single"
).load()

# 切分为文本块
chunks = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", "。", "！", "？", "……", "，", ""],  # 分隔符优先级列表
    chunk_size=400,        # 每个块的最大长度
    chunk_overlap=50,      # 相邻块重叠长度
    length_function=len,   # 长度计算函数
).split_documents(docs)

# 统计块数量
print(f"切分得到 {len(chunks)} 个文本块\n")

# 可选：查看前几个块内容和元数据
for i, chunk in enumerate(chunks[:5]):  # 只看前 5 个
    print(f"=== Chunk {i} ===")
    print(chunk.page_content)
    print("metadata:", chunk.metadata)
    print("============\n")

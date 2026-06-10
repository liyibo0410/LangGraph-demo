# 第 1 部分：导入依赖（工具包）
# uv add FlagEmbedding==1.3.5               #安装命令，用 uv 提前装好库（只需要执行一次）
# uv add transformers==4.44.2               #安装命令，用 uv 提前装好库（只需要执行一次）
from FlagEmbedding import BGEM3FlagModel    #from xxx import xxx：固定语法，从第三方库里拿出我们要用的类
                                            #BGEM3FlagModel：专门加载 bge-m3 模型、计算混合向量的工具类
# $模板：from 库名 import 工具类


# 第 2 部分：加载本地模型（核心初始化）
model = BGEM3FlagModel(model_name_or_path=r"D:\software\ai_models\huggingface_cache\bge-m3")
# 1.model = 变量名：把加载好的模型存到变量 model，后面反复调用
# 2.BGEM3FlagModel( 参数 )：实例化模型，括号里传模型本地文件夹路径
# 3.r"路径"：Windows 路径必须加r，防止\被程序识别成转义字符
# $模板：变量 = 模型类( model_name_or_path=r"你的模型文件夹完整路径" )

# 第 3 部分：准备要向量化的文本
text = "标量字段通常用来存储一些元数据，并可以在搜索时通过元数据进行过滤"
# 1.text：自定义变量，存你要处理的句子 / 段落
# 2.字符串用双引号 / 单引号包裹都行
# $模板：变量名 = "你的文本内容"


# 第 4 部分：调用模型编码，生成稠密 + 稀疏向量（核心计算）
res = model.encode(          # model.encode()：模型自带的编码函数，输入文本输出向量结果
    [text],         # 第一个参数 [text]：必须传列表，支持批量传入多条文本，比如 [text1, text2, text3]
    return_sparse=True,      # return_dense=True：开启输出稠密向量（整条文本语义）
    return_dense=True        # return_sparse=True：开启输出稀疏词权重（关键词）
)

# 结果存到 res 字典里，res 包含 dense_vecs（稠密向量）、lexical_weights（稀疏权重）
# $模板：结果变量 = 模型变量.encode([文本1,文本2], return_dense=True, return_sparse=True)


# 第 5 部分：打印原始文本
print("=== 原始文本 ===")
print(text)
print("=" * 50)


# 第 6 部分：读取稀疏向量 ID + 权重（机器可读格式）
# 1. 稀疏向量（关键词及其权重，原始 id 形式）
print("=== 稀疏向量（id → 权重）===")
lexical_weights = res["lexical_weights"][0]  # batch 中第一条
# 只看前若干个，避免太长
for i, (token_id, weight) in enumerate(list(lexical_weights.items())[:20]):
    print(f"[{i:02d}] id={token_id:<5}  weight={weight:.4f}")
print("...（仅展示前 20 个）")
print("=" * 50)
# 逐行拆解：
# res["lexical_weights"][0]
# res["键名"]：读取字典里对应数据；lexical_weights 是稀疏权重列表
# [0]：因为我们只传了 1 条文本，取第 0 个结果（多条文本就取对应下标）
# lexical_weights.items()：把 {分词 ID: 权重} 字典拆成一对对 (id, weight)
# list(...)[ :20 ]：只取前 20 个关键词，防止输出刷屏
# for i, (token_id, weight) in enumerate(xxx)
# enumerate：自动生成序号 i
# 循环每一组分词 ID 和权重
# f"[{i:02d}] id={token_id:<5} weight={weight:.4f}" f-string 格式化
# :02d：序号补 0，变成 00、01、02 整齐排版
# :.4f：权重保留 4 位小数


# 第 7 部分：把数字 ID 转成汉字 / 词语（人能看懂）
# 2. 把稀疏向量的 id 转成可读 token
print("=== 稀疏向量（token → 权重）===")
sparse_tokens = model.convert_id_to_token(lexical_weights)

for i, (token, weight) in enumerate(list(sparse_tokens.items())[:20]):
    print(f"[{i:02d}] token='{token}'  weight={weight:.4f}")
# model.convert_id_to_token(权重字典)：模型自带转换函数，数字 ID → 对应汉字词语
# 循环逻辑和上一段完全一样，只是打印词语而非数字 ID


# 第 8 部分：读取并打印稠密向量
# 3. 稠密向量（1024 维）
dense_vec = res["dense_vecs"][0]

print("=== 稠密向量信息 ===")
print(f"维度: {len(dense_vec)}")
print("前 10 维示例:")
print([round(x, 4) for x in dense_vec[:10]])
# res["dense_vecs"][0]：读取第一条文本的稠密向量数组
# len(dense_vec)：获取向量长度，bge-m3 固定 1024 维
# [round(x,4) for x in dense_vec[:10]] 列表推导式：
# 取前 10 个数字，每个保留 4 位小数，整洁输出
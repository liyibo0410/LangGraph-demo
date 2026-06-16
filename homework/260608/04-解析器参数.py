from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

# 1. 定义一个简单的数据模型
class Character(BaseModel):
    name: str = Field(description="角色名字")
    skill: str = Field(description="核心技能")

# 2. 模拟大模型在流式输出（Streaming）时，中途吐出的“不完整/半截”JSON 文本
# 注意：此时括号没闭合，字段也不全
half_token_1 = '{"name": "孙悟空"'
half_token_2 = '{"name": "孙悟空", "skill": "七十二变'
full_token   = '{"name": "孙悟空", "skill": "七十二变"}'

# # =====================================================================
# # 场景一：使用 partial=True（适配边生成边解析）
# # =====================================================================
# parser_lazy = JsonOutputParser(pydantic_object=Character, partial=True)
#
# print("--- 测试 partial=True ---")
# # 刚吐出第一个片段：能解析多少就返回多少
# print(f"片段 1 解析结果: {parser_lazy.parse(half_token_1)}")
# # 输出: {'name': '孙悟空'}
#
# # 吐出第二个片段：哪怕 value 没写完，也能把结构保留
# print(f"片段 2 解析结果: {parser_lazy.parse(half_token_2)}")
# # 输出: {'name': '孙悟空', 'skill': '七十二变'}

# =====================================================================
# 场景二：使用 partial=False（默认值，要求严格完整）
# =====================================================================
parser_strict = JsonOutputParser(pydantic_object=Character, partial=False)

print("\n--- 测试 partial=False ---")
try:
    # 尝试解析不完整的片段，会直接引发异常
    parser_strict.parse(half_token_1)
except Exception as e:
    print(f"片段 1 解析失败 ❌ 触发异常:\n{e}")

# 只有传入完全合法的 JSON，它才放行
print(f"完整片段解析结果: {parser_strict.parse(full_token)}")
# 输出: {'name': '孙悟空', 'skill': '七十二变'}
# 使用纯字典做状态定义的风险
# 1. 拼写错误，运行时才能发现
# 2. 数据类型模糊
from typing import Dict, Any

# 标注：user_state 是 字符串键、任意值 的字典
user_state = Dict[str, Any]
user_state = {
    "name": "Peter",
    "age": 20
}

print(user_state["name"])
print(user_state["age"])

# 运行时动态新增字段
user_state["score"] = 99.0
print(user_state["score"])
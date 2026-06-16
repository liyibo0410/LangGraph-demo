# 03_state/02_TypedDict_UserState_demo.py
from typing import TypedDict

# 1. 定义结构（像画图纸一样）
class UserState(TypedDict):
    name: str  # 规定 name 必须是字符串
    age: int   # 规定 age 必须是整数

# 2. 实例化时，它就像一个普通字典
user_state: UserState = {
    "name": "Alice",
    "age": 25
}
print(user_state)

# 3. 提前拦截错误
# 当你输入其他键时，IDE会告诉你只能填 "name" 或 "age"
print(user_state["name"])
# 如果你不小心把 "age" 拼成了 "egg"
# 编写代码时IDE就会提示
# print(user_state["egg"])
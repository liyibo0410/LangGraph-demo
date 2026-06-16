# 03_state/04_Pydantic_UserState_demo.py

from pydantic import BaseModel

# 1. 定义结构
class UserState(BaseModel):
    name: str
    age: int

# 2. 实例化时，必须通过类调用，且会自动校验类型
# user_state = UserState(name="Bob", age=30)
user_state = UserState(name="Bob", age="30") # 注意：即使传入字符串"30"，Pydantic也会自动转为整数

print(user_state)
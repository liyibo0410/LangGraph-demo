# 03_state/06_dataclass_UserState_demo.py

from dataclasses import dataclass

# 2. 使用dataclass装饰器，自动生成__init__()和__repr__()方法
@dataclass
# 1. 创建数据类
class UserState:
    name: str
    age: int

    # def __init__(self, name: str, age: int):
    #     self.name = "Charlie"
    #     self.age = 35
    #
    # def __repr__(self):
    #     return f"UserState(name={self.name}, age={self.age})"

# 2. 实例化
user_state = UserState(name="Charlie", age=35)

# 3. 打印时会直接显示内容，不需要额外写打印函数
print(user_state) # 输出: UserState(name='Charlie', age=35)
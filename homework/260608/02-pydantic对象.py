# class Dog:
#     name: str
#     age: int
#     address: str
#
#
# d = Dog()
# from pydantic import BaseModel, Field
#
#
# from pydantic import BaseModel
#
# class Dog(BaseModel):
#     name: str
#     age: int
#
# d = Dog()  # 报错！必须传参数！

# def test(a:int):
#     print(a)
#
# test("abc")


class User(BaseModel):
    name: str
    age: int
    email: str = Field(description='用户的邮箱地址')

#
# user = User(name='张三', age=20, email='wwy@123.com')
# print(user.name)
# print(user.age)
# user2 = User(name='李四',age='abc',email='123@qq.com')
# print(user2.age)
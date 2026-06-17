# 04_nodes/04_intern_demo.py
import sys  # 导入系统内置模块，使用intern驻留函数

# ========== 第一部分：手动使用 sys.intern 强制驻留字符串 ==========
# "hello" + " world" 运行时拼接得到新字符串，再交给 sys.intern
# intern作用：把字符串存入全局驻留池，后续相同内容直接复用内存地址
str1 = sys.intern("hello" + " world")
str2 = sys.intern("hello" + " world")

print(str1 == str2)       # True  == 比较两个字符串【内容】是否相等
print(str1 is str2)       # True  is 比较两个变量【内存地址】是否完全同一个对象
print(id(str1))           # id() 打印对象内存地址，两个变量地址一致
print(id(str2))           # 和str1 id完全相同，复用驻留池里的同一个字符串对象


# ========== 第二部分：编译器自动常量折叠（无需intern） ==========
# 直接写死常量字符串字面量，Python编译阶段自动做常量折叠+驻留优化
# 编译器识别两个完全一样的常量，只创建一份内存
str3 = "hello world"
str4 = "hello world"
print(str3 == str4)       # True 内容完全一致
print(str3 is str4)       # True 内存地址相同，自动驻留生效
print(id(str3))           # 内存地址和上面str1/str2是同一个
print(id(str4))           # 和str3 id完全一致

"""
# 核心知识点总结
1. == 和 is 的区别
- == ：只对比字符串内容，内容一样就返回True
- is ：对比内存地址，只有两个变量指向堆中同一个对象才返回True

2. sys.intern() 字符串驻留机制
- 原理：维护一个全局字符串驻留池，存入过的字符串不会重复开辟内存
- 适用场景：大量重复动态拼接字符串（循环、接口返回、拼接生成字符串），节省内存、提升比较速度
- 动态拼接字符串（运行时拼接）默认不会自动驻留，必须手动intern

3. 自动常量折叠（编译期优化）
代码写死固定字面量 "hello world"，Python在编译代码时直接合并优化，
不需要调用intern，自动复用同一块内存。

4. 对比反例（不加intern的动态拼接）
a = "hello"
b = a + " world"
c = a + " world"
print(b is c)  # False，动态拼接生成两个不同对象，地址不一样
如果改成 b = sys.intern(a + " world") 就会地址相同
"""
# 04_nodes/05_str_demo.py
# 1. 常量字面量字符串：编译期直接确定内容，自动驻留
str1 = "hello world"

# 2. f-string动态拼接：运行时拼接生成字符串，属于动态字符串
name = "world"
str2 = f"hello {name}"

print("\n--- 比较 str1 和 str2 (f-string 动态生成) ---")
# id() 查看变量在内存中的唯一地址
print(f"str1内存地址: {id(str1)}")
print(f"str2内存地址: {id(str2)}")

# == 判断：只对比字符串文字内容是否一样
print(f"内容相同 (==): {str1 == str2}")  # True，两段文字都是hello world

# is 判断：对比内存地址，是否是同一个对象
print(f"地址相同 (is): {str1 is str2}")  # False，两块独立内存

"""
# 核心知识点讲解
1. 什么时候自动驻留？
只有**编译期就能完全确定**的常量字符串才会自动放入驻留池：
例：a = "hello world"、b = "hello" + " world"

2. f-string 为什么不自动驻留？
f-string中包含变量 {name}，变量的值是运行时才读取的，
编译器无法提前算出最终字符串，属于动态字符串，不会自动驻留，会新建内存对象。

3. 解决办法：手动使用 sys.intern 强制驻留
import sys
name = "world"
str2 = sys.intern(f"hello {name}")
此时 str1 is str2 → True

4. == 与 is 核心区别
- ==：比对内容，只看文字一不一样
- is：比对内存地址，必须是同一个内存对象才返回True
"""
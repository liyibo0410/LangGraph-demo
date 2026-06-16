import base64
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(model="Pro/moonshotai/Kimi-K2.6")  # 需要使用支持视觉语言的模型（VLM模型:视觉语言模型 LLM模型）
# 视觉模型：只能看懂图片的内容(OCR---yolox yolo-v8)
# 视觉语言模型：即能看懂图片内容 也能把看到的内容输出出来（VLM:各个平台都有各种各样的视觉模型）

# 读取图片
with open("imgs/zlh.jpg", "rb") as f:
    image_data = f.read()


# print(image_data)


message = HumanMessage(content=[
    {"type": "text", "text": "描述这张图片"},
    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64.b64encode(image_data).decode()}"}}
])
print(message)
# response = llm.invoke([message])
# print(response.content)




# import base64
#
# # 编码
# with open("./imgs/image.jpg", "rb") as f:
#     binary_data = f.read()                                # bytes: 原始二进制
#     base64_bytes = base64.b64encode(binary_data)          # bytes: Base64 编码后仍是 bytes 类型
#     base64_string = base64_bytes.decode("utf-8")          # str:   转成字符串（Python 类型要求）
#
# # .decode("utf-8") 的作用：
# # Python 的 b64encode 返回 bytes 类型，但 JSON/f-string 需要 str 类型
# # 因为 Base64 输出全是 ASCII 字符，所以这里只是做类型转换，不涉及字符编码解读
#
# # 解码
# binary_data = base64.b64decode(base64_string)
# print(binary_data)





from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI

# 第一步：准备示例数据
examples = [
    {"input": "高兴", "output": "开心"},
    {"input": "难过", "output": "悲伤"},
    {"input": "生气", "output": "愤怒"}
]

# 第二步：定义单条示例的格式化模板
example_formatter = PromptTemplate(
    template="输入: {input}\n输出: {output}",
    input_variables=["input", "output"]
)

# 第三步：创建少样本提示模板
fsp = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_formatter,
    prefix="以下是一些同义词转换的例子：",    # 示例前的说明文字
    suffix="\n输入: {input}\n输出:",         # 示例后的实际问题
    input_variables=["input"]
)

# # 调用
# print(few_shot_prompt.invoke({"input": "兴奋"}))

llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V4-Flash"
)
print(llm.invoke(fsp.invoke({"input": "兴奋"})).content)
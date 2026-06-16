from langchain_core.output_parsers import BaseOutputParser, StrOutputParser, JsonOutputParser


class DemoOutputParser(BaseOutputParser):
    def parse(self, text: str):
        return [item.strip() for item in text.split(':')]

# StrOutputParser
# JsonOutputParser
p = DemoOutputParser() # 自定义的 输出解析器
res = p.parse("苹果:香蕉:橘子")
print(res)

# 必加：加载.env环境变量
from dotenv import load_dotenv   #读取环境配置文件的第三方工具库
load_dotenv()                    #读取.env文件，把里面的配置存入系统环境变量os.environ

#导入所有需要的工具包
import os                        #系统工具，用来读取刚才.env存好的 AI 密钥、接口地址
from langchain_core.output_parsers import JsonOutputParser
# langchain_core：   LangChain 核心基础功能包，所有通用工具都在这里
# JsonOutputParser： LangChain 自带的「JSON 格式管控工具」
# 两大功能：
# ① 告诉 AI：你必须按 JSON 格式回答；
# ② AI 回答完，自动把文字 JSON 转成 Python 字典
from langchain_openai import ChatOpenAI   #国产通用 AI 调用工具
from pydantic import BaseModel, Field     #制作回答模板的工具，规定 AI 输出有哪些字段、每个字段写什么内容
# pydantic：数据校验工具，用来定义固定数据模板

# 大模型配置，连接 AI 大模型（初始化客户端）
llm = ChatOpenAI(                               #LLM大语言模型实例
    model="deepseek-ai/DeepSeek-V4-Flash",      #model：你要调用的 AI 模型名字
    temperature=0.7,                            #temperature=0.7：AI 脑洞大小。0 = 死板固定，1 = 天马行空；
    base_url=os.getenv("SILICON_BASE_URL"),     #base_url：AI 服务的网络地址，从.env 配置文件读取，不写死代码
    api_key=os.getenv("SILICON_API_KEY")        #api_key：你的账号密钥，用来登录 AI 平台扣额度，从.env 读取
)

# 定义JSON结构
class Joke(BaseModel):                          #自定义数据模式（Schema），继承 Pydantic 基础模板类
    title: str = Field(description='笑话的标题,简洁有趣')
    content: str = Field(description='笑话的正文内容,幽默诙谐')            #字段名 + 类型约束
    theme: str = Field(description='笑话的主题,比如 日常、职场、动物')
                #Field(description="xxx")：字段元描述，会直接传给 AI，告诉 AI 这个字段该填什么内容

# JSON解析器
jsp = JsonOutputParser(pydantic_object=Joke)

# 调用模型
res = llm.invoke([
    ('system', jsp.get_format_instructions()),
    ('human', "请你给我讲一个笑话,幽默诙谐")
])

# 输出原始内容
print(res.content)
print(type(res.content))

# 解析成字典
pe = jsp.invoke(res.content)

print("---------------------")
print(type(pe))  # <class 'dict'>
print(pe['title'])
print(pe['content'])
print(pe['theme'])
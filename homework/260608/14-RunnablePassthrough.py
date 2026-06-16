from langchain_core.runnables import RunnableLambda

# 函数1：从URL里拿出域名
def extract_domain(url):
    return url.split('//')[-1].split('/')[0]

# 函数2：给域名加上 http://
def add_protocol(domain):
    return f"http://{domain}"

# 把普通函数包装成 LangChain 组件
domain_extractor = RunnableLambda(extract_domain)
protocol_adder = RunnableLambda(add_protocol)

# 用 | 串成一条链：函数1 → 函数2
chain = domain_extractor | protocol_adder

# 调用
result = chain.invoke("https://www.example.com/path")

print(result)  # 输出：http://www.example.com
from openai import OpenAI
import json

# ===================== 硅基流动配置 =====================
SILICON_API_KEY = "sk-ducppopfynsqzackdlrumezrgnronsikpcaneceontoxpxoz"
SILICON_BASE_URL = "https://api.siliconflow.cn/v1"

# 初始化硅基流动客户端
client = OpenAI(
    api_key=SILICON_API_KEY,
    base_url=SILICON_BASE_URL
)
# ======================================================

# ===== 第1步：工具JSON Schema描述（删掉strict:true兼容V4-Flash） =====
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市在指定日期的天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称",
                    },
                    "date": {
                        "type": "string",
                        "description": "日期，格式为YYYY-MM-DD",
                    }
                },
                "required": ["city", "date"],
                "additionalProperties": False,
            }
            # 移除 strict: True，DeepSeek V4-Flash 易解析失败
        },
    },
]

# ===== 第2步：本地工具执行函数 =====
def get_weather(city, date):
    return f"{city} 在 {date} 天气多云，有下雨的可能性。"

# ===== 第3步：用户对话初始消息 =====
messages = [
    {"role": "user", "content": "河南洛阳栾川县2026-6-15的天气怎么样？"}
]

# 第一轮：让模型判断是否调用工具
response = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V4-Flash",  # 硅基标准完整模型ID
    messages=messages,
    tools=tools,
)

# 把模型返回的工具调用消息加入上下文
assistant_msg = response.choices[0].message
messages.append(assistant_msg)

# 处理工具调用
tool_calls = assistant_msg.tool_calls
if tool_calls:
    for tool_call in tool_calls:
        if tool_call.function.name == "get_weather":
            # 解析参数
            args = json.loads(tool_call.function.arguments)
            # 执行本地工具
            weather_result = get_weather(args["city"], args["date"])
            # 工具结果回填对话
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps({"weather": weather_result}),
            })

# 第二轮：传入工具结果，生成最终自然语言回答
final_response = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V4-Flash",
    messages=messages,
    tools=tools,
)

# 打印最终输出
print(final_response.choices[0].message.content)
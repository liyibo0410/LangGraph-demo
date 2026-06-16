from langchain.tools import tool

@tool
def get_weather(city: str, date: str) -> str:
    """获取指定城市在指定日期的天气。

    Args:
        city: 城市名称，如"北京"、"上海"
        date: 日期，格式为YYYY-MM-DD
    """
    # 实际项目中调用天气API，这里用模拟数据
    return f"{city} 在 {date} 天气多云，有下雨的可能性。"
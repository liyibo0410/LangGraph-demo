from langchain.tools import tool
from pydantic import BaseModel, Field

class GetWeatherArgs(BaseModel):
    """天气查询参数"""
    city: str = Field(description="城市名称，如'北京'、'上海'")
    date: str = Field(description="查询日期，格式为YYYY-MM-DD")

@tool(args_schema=GetWeatherArgs)
def get_weather(city: str, date: str) -> str:
    """获取指定城市在指定日期的天气预报"""
    return f"{city} 在 {date} 天气多云，有下雨的可能性。"
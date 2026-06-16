import os
import requests
from dotenv import load_dotenv

# 加载.env配置
load_dotenv()
token = os.getenv('MINERU_TOKEN')

# ==================== 1. 提交解析任务（加载在线pdf） ====================
submit_url = "https://mineru.net/api/v4/extract/task"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}
data = {
    "url": "https://cdn-mineru.openxlab.org.cn/demo/example.pdf",
    "model_version": "vlm"
}

res = requests.post(submit_url, headers=headers, json=data)
print("提交任务状态码：", res.status_code)
resp_json = res.json()
print("提交任务返回：", resp_json)

# 自动获取新的 task_id
task_id = resp_json["data"]["task_id"]
print("新任务ID：", task_id)

# ==================== 2. 获取解析结果（自动轮询） ====================
query_url = f"https://mineru.net/api/v4/extract/task/{task_id}"

import time

for i in range(20):  # 最多等20次
    time.sleep(2)
    res = requests.get(query_url, headers=headers)
    task_data = res.json()["data"]

    print(f"\n第{i + 1}次查询状态：", task_data["state"])

    if task_data["state"] == "done":
        print("\n✅ 解析完成！")
        print("📦 压缩包下载地址：", task_data["full_zip_url"])
        break
    elif task_data["state"] == "failed":
        print("❌ 解析失败")
        break
# ==================== 加载环境变量 & 导入依赖 ====================
import os
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()
token = os.getenv("MINERU_TOKEN")

# ==================== 1. 上传本地 PDF 文件 ====================
def mineru_upload_file_demo():
    if not token:
        raise RuntimeError("环境变量 MINERU_TOKEN 未设置")

    # 1. 申请上传 URL
    url = "https://mineru.net/api/v4/file-urls/batch"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    # 本地文件路径（改成你自己的）
    file_paths = [
        r"test_mini.pdf"
    ]

    files_info = []
    for i, p in enumerate(file_paths):
        p = Path(p)
        if not p.exists():
            raise FileNotFoundError(f"文件不存在: {p}")
        files_info.append({
            "name": p.name,
            "data_id": f"data_{i}",
        })

    data = {
        "files": files_info,
        "model_version": "vlm",
    }

    resp = requests.post(url, headers=headers, json=data)
    if resp.status_code != 200:
        print(f"申请上传URL失败：{resp.status_code}")
        return None

    result = resp.json()
    if result.get("code") != 0:
        print(f"失败原因：{result.get('msg')}")
        return None

    batch_id = result["data"]["batch_id"]
    urls = result["data"]["file_urls"]
    print(f"✅ 申请上传成功，batch_id: {batch_id}")

    # 2. 上传文件
    for i, upload_url in enumerate(urls):
        path = Path(file_paths[i])
        with path.open("rb") as f:
            res_upload = requests.put(upload_url, data=f)
        if res_upload.status_code == 200:
            print(f"✅ {path.name} 上传成功")
        else:
            print(f"❌ {path.name} 上传失败")

    return batch_id

# ==================== 2. 轮询查询解析结果 ====================
def mineru_check_result_demo(batch_id: str, max_retries: int = 30, interval: int = 3):
    url = f"https://mineru.net/api/v4/extract-results/batch/{batch_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    for i in range(max_retries):
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            print(f"请求失败，状态码：{resp.status_code}")
            return None

        data = resp.json()
        extract_list = data.get("data", {}).get("extract_result", [])
        if not extract_list:
            print("暂无解析结果，继续等待...")
            time.sleep(interval)
            continue

        item = extract_list[0]
        state = item.get("state")
        print(f"第 {i+1} 次查询 → 状态：{state}")

        if state == "done":
            full_zip_url = item.get("full_zip_url")
            print("\n🎉 解析完成！")
            print("📦 结果下载地址：", full_zip_url)
            return full_zip_url
        elif state in ("failed", "error"):
            print("❌ 解析失败")
            return None

        time.sleep(interval)

    print("⏰ 超时未完成")
    return None

# ==================== 3. 一键执行 ====================
if __name__ == "__main__":
    batch_id = mineru_upload_file_demo()
    if batch_id:
        mineru_check_result_demo(batch_id)

import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def get_toutiao_news():
    """爬取今日头条热门新闻"""
    url = "https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://www.toutiao.com/",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 检查请求是否成功
        
        data = response.json()
        if data.get("data") and isinstance(data["data"], list):
            # 提取前10条新闻
            news_list = []
            for item in data["data"][:10]:
                news = {
                    "title": item.get("Title", ""),
                    "hot": item.get("HotValue", 0),
                    "url": item.get("Url", ""),
                    "time": item.get("PublishTime", "")
                }
                news_list.append(news)
            
            return news_list
        else:
            print("未获取到新闻数据:", data)
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"请求出错: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"解析JSON出错: {e}")
        return []
    except Exception as e:
        print(f"发生未知错误: {e}")
        return []

def save_news(news_list):
    """保存新闻到JSON文件"""
    if not news_list:
        print("没有新闻数据可保存")
        return
    
    # 创建存储目录（如果不存在）
    data_dir = os.path.join(os.path.dirname(__file__), "news_data")
    os.makedirs(data_dir, exist_ok=True)
    
    # 使用当前日期时间作为文件名
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    file_path = os.path.join(data_dir, f"{timestamp}.json")
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(news_list, f, ensure_ascii=False, indent=2)
        print(f"新闻已保存到 {file_path}")
    except Exception as e:
        print(f"保存文件出错: {e}")

if __name__ == "__main__":
    print("开始爬取今日头条热门新闻...")
    news = get_toutiao_news()
    save_news(news)
    print("爬取完成")    

# 使用说明：

# 1. 将上述代码保存到 GitHub 仓库中，确保文件结构如下：
#    - `toutiao_crawler.py`
#    - `.github/workflows/crawl-news.yml`

# 2. 该脚本会：
#    - 爬取今日头条的热门新闻榜单
#    - 提取前10条新闻的标题、热度、链接和发布时间
#    - 将数据保存为JSON格式，文件名使用当天日期
#    - 每天自动运行并更新数据

# 3. 注意事项：
#    - 爬取频率已设置为每天一次，避免频繁请求
#    - 数据存储在仓库的 `news_data` 目录下
#    - 如需调整爬取时间，可修改 `crawl-news.yml` 中的 cron 表达式
#    - 脚本使用了请求头模拟浏览器访问，降低被封的风险

# 这个方案完全在 GitHub 上自动运行，无需本地环境支持。爬取的新闻数据会以 JSON 格式保存在仓库中，方便查看和使用。

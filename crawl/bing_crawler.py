import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def get_bing_news():
    """爬取必应新闻"""
    url = "https://cn.bing.com/hp/api/v1/carousel?&format=json&ecount=20&efirst=0&features=tobads&ads=1&features=tobcnads"
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh-TW;q=0.9,zh;q=0.8,en;q=0.7,en-US;q=0.6",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "referer": "https://cn.bing.com/"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        news_items = []
        for item in data['data'][0]['items']:
            news_items.append({
                'title': item['title'],
                'url': 'https://cn.bing.com' + item['url'],
                'image': 'https://cn.bing.com' + item['imageUrl'] if item['imageUrl'] else None
            })
        
        return news_items
        
    except requests.exceptions.RequestException as e:
        print(f"请求出错: {e}")
        return []
    except Exception as e:
        print(f"解析出错: {e}")
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
    file_path = os.path.join(data_dir, f"bing_{timestamp}.json")
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(news_list, f, ensure_ascii=False, indent=2)
        print(f"新闻已保存到 {file_path}")
    except Exception as e:
        print(f"保存文件出错: {e}")

if __name__ == "__main__":
    print("开始爬取必应新闻...")
    news = get_bing_news()
    save_news(news)
    print("爬取完成")

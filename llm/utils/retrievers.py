import re
import traceback
import json
import httpx

from urllib.parse import quote
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/124.0.0.0 Safari/537.36"
}


def get_page_pure_text(html_text: str):
    # 提取文字
    pure_text = BeautifulSoup(html_text, "html.parser").get_text()
    pure_text = re.sub(r'\s+', '\n', pure_text).strip()
    return pure_text


async def search_bing(query: str):
    """必应搜索"""
    query = quote(query)
    url = f"https://cn.bing.com/search?q={query}"
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers)
        pure_text = get_page_pure_text(r.text)
        return pure_text


async def search_tavily(query: str, api_key: str = None, max_results=5):
    """泰维利亚搜索"""
    url = "https://api.tavily.com/search"

    data = {
        "api_key": api_key,
        "query": query,
        "search_depth": "basic",
        "include_answer": False,
        "include_images": False,
        "include_raw_content": False,
        "max_results": max_results,
        "include_domains": [],
        "exclude_domains": []
    }
    async with httpx.AsyncClient() as client:
        try:
            r = await client.post(url, headers=headers, json=data)
            print(r.text)
            results = r.json()["results"]
            return json.dumps(results, ensure_ascii=False)
        except Exception as e:
            print(e)
            return "内容提取失败"


async def get_url_content(url: str):
    """提取指定页面内容"""
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(url, headers=headers)
            pure_text = get_page_pure_text(r.text)
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            return "内容提取失败"
        return pure_text

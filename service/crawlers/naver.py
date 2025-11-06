import requests
import json
from datetime import datetime, timedelta

NAVER_API_URL = "https://openapi.naver.com/v1/datalab/search"

def get_naver_datalab_interest(keyword, NAVER_CLIENT_ID, NAVER_CLIENT_SECRET):
    HEADERS = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
        "Content-Type": "application/json"
    }

    today = datetime.now()
    end_date = today.strftime("%Y-%m-%d")
    start_date = (today - timedelta(days=30)).strftime("%Y-%m-%d")

    payload = {
        "startDate": start_date,
        "endDate": end_date,
        "timeUnit": "date",
        "keywordGroups": [
            {
                "groupName": keyword,
                "keywords": [keyword]
            }
        ]
    }

    response = requests.post(
        NAVER_API_URL,
        headers=HEADERS,
        data=json.dumps(payload)
    )
    response.raise_for_status()

    data = response.json()

    result_data = data.get('results', [])[0].get('data', [])

    if not result_data:
        return {'naver_datalab_daily_ratio': 0}

    last_day_data = result_data[-1]
    yesterday_ratio = last_day_data.get('ratio')

    return {'naver_datalab_daily_ratio': yesterday_ratio}


def get_naver_mentions_24h(keyword, NAVER_CLIENT_ID, NAVER_CLIENT_SECRET):
    NAVER_API_URL_BLOG = "https://openapi.naver.com/v1/search/blog.json"
    NAVER_API_URL_CAFE = "https://openapi.naver.com/v1/search/cafearticle.json"
    HEADERS = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
    }

    api_urls = [NAVER_API_URL_BLOG, NAVER_API_URL_CAFE]
    total_count_24h = 0

    params = {
        'query': keyword,
        'display': 100,
        'sort': 'date'
    }

    for api_url in api_urls:
        api_name = "블로그" if "blog" in api_url else "카페"

        response = requests.get(api_url, headers=HEADERS, params=params)
        response.raise_for_status()

        data = response.json()
        items = data.get('items', [])

        if not items:
            print(f"[NaverCrawler] '{keyword}' {api_name} 검색 결과 없음")
            continue

        now = datetime.now()
        yesterday = now - timedelta(days=1)

        for item in items:
            post_time = None
            if 'postdate' in item:
                date_str = item['postdate']
                post_time = datetime.strptime(date_str, "%Y%m%d")
            elif 'pubDate' in item:
                date_str = item['pubDate']
                post_time = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
                post_time = post_time.replace(tzinfo=None)

            if post_time and post_time >= yesterday:
                total_count_24h += 1
            elif post_time and post_time < yesterday:
                break

    return {'naver_mentions_24h': total_count_24h}
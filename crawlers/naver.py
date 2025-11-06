import requests
import json
from datetime import datetime, timedelta
import dotenv
import os

dotenv.load_dotenv()

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

NAVER_API_URL = "https://openapi.naver.com/v1/datalab/search"

def get_naver_datalab_interest(keyword):
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


if __name__ == '__main__':
    TEST_KEYWORD = "한로로"  # 테스트할 키워드
    stats = get_naver_datalab_interest(TEST_KEYWORD)
    print(f"--- Naver DataLab '{TEST_KEYWORD}' 최종 결과 ---", stats)
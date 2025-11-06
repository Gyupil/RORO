import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}

def get_dcinside_mentions_24h():
    print(f"[DCInsideCrawler] 24시간 내 언급량 크롤링 시작...")

    done = False
    num = 1
    try:
        while not done:
            DC_SEARCH_URL = f"https://search.dcinside.com/post/p/{num}/q/.ED.95.9C.EB.A1.9C.EB.A1.9C"
            response = requests.get(DC_SEARCH_URL, headers=HEADERS)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            search_list_selector = "div.integrate_cont.sch_result ul.sch_result_list > li"
            search_list = soup.select(search_list_selector)

            now = datetime.now()
            yesterday = now - timedelta(days=1)
            count_24h = 0

            for item in search_list:
                title = item.find('a', class_="tit_txt").get_text(strip=True)
                what = item.find('p', class_="link_dsc_txt").get_text(strip=True)
                what2 = item.find('p', class_="link_dsc_txt dsc_sub").get_text(strip=True)

                if '한로로' not in title and '한로로' not in what and '한로로' not in what2:
                    continue

                date_element = item.find('span', class_='date_time')
                if not date_element:
                    continue

                date_str = date_element.text.strip()

                post_time = None
                if re.fullmatch(r"\d{2}:\d{2}", date_str):
                    hour, minute = map(int, date_str.split(':'))
                    post_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                elif re.fullmatch(r"\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}", date_str):
                    post_time = datetime.strptime(date_str, "%Y.%m.%d %H:%M")

                if post_time and post_time >= yesterday:
                    count_24h += 1
                elif post_time and post_time < yesterday:
                    done = True
                    break

            num += 1

        print(f"[DCInsideCrawler] 24시간 내 언급된 게시물 수: {count_24h}건")
        return {'dc_mentions_24h': count_24h}

    except requests.exceptions.RequestException as e:
        print(f"[DCInsideCrawler] 요청 오류 발생: {e}")
        return {'dc_mentions_24h': 0}
    except Exception as e:
        print(f"[DCInsideCrawler] 알 수 없는 오류 발생: {e}")
        return {'dc_mentions_24h': 0}


if __name__ == '__main__':
    stats = get_dcinside_mentions_24h()
    print("--- DCInside 최종 결과 ---", stats)
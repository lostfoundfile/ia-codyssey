import requests
from bs4 import BeautifulSoup


def get_kbs_headlines():
    """
    KBS 주요 뉴스 헤드라인을 크롤링하여 리스트로 반환한다.
    """
    url = 'http://news.kbs.co.kr'
    response = requests.get(url, timeout=5)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    # 개발자 도구 확인 → 주요 뉴스 헤드라인이 포함된 선택자 탐색 필요
    # (2025년 9월 기준 KBS 사이트 구조 예시: headline 영역 a 태그)
    headlines = []
    headline_tags = soup.select('div.news-today section.section-main a')

    for tag in headline_tags:
        text = tag.get_text(strip=True)
        if text:
            headlines.append(text)

    return headlines


def main():
    headlines = get_kbs_headlines()
    print('KBS 주요 뉴스 헤드라인:')
    for idx, title in enumerate(headlines, start=1):
        print(f'{idx}. {title}')


if __name__ == '__main__':
    main()
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from pymongo import MongoClient

# pymongo를 임포트 하기
client = MongoClient('localhost', 27017)
# mongoDB는 27017 포트로 돌아갑니다.
db = client.testDB

# 드라이버 열기
driver = webdriver.Chrome('./chromedriver')

# KBO 2018년도 선수스탯 크롤링 함수
def crawler(teams):
    collection = db[teams]
    # URL 가져오기
    driver.get('https://www.koreabaseball.com/Record/Player/HitterBasic/Basic1.aspx')
    # 스탯 옵션에서 팀 선택하
    driver.find_element_by_xpath(f"//select[@name='ctl00$ctl00$ctl00$cphContents$cphContents$cphContents$ddlTeam$ddlTeam']/option[text()='{teams}']").click()
    # 3초 스톱
    time.sleep(3)
    driver.find_element_by_xpath('//a[@href="'+"javascript:sort('GAME_CN');"+'"]').click()
    time.sleep(3)
    # 해당 페이지의 html 소스 선택
    html = driver.page_source
    # html 파싱하기
    soup = BeautifulSoup(html, 'html.parser')
    # tr 태그내용 가져오기
    players = soup.select('div.record_result > table > tbody > tr')

    rank = 1
    # tr 태그 내 선수 스탯 출력하기
    for player in players:
        name = player.select_one('td > a').text  # 이름
        team = player.find_all('td')[2].text
        href = "https://www.koreabaseball.com" + player.select_one('td > a')['href']  # 선수 개별 페이지 링크
        game = player.find('td', {'data-id': 'GAME_CN'}).text # 경기
        avg = player.find('td', {'data-id': 'HRA_RT'}).text  # 타율
        run = player.find('td', {'data-id': 'RUN_CN'}).text  # 득점
        hit = player.find('td', {'data-id': 'HIT_CN'}).text  # 안타
        hr = player.find('td', {'data-id': 'HR_CN'}).text  # 홈런
        rbi = player.find('td', {'data-id': 'RBI_CN'}).text  # 타점

        # 선수 개별 페이지 들어가기
        driver.get(href)
        # 해당 페이지의 html 소스 선택
        html = driver.page_source
        # html 파싱하기
        soup = BeautifulSoup(html, 'html.parser')
        # 이미지 태그 가져오기
        photo = soup.select_one('div.photo > img')
        # 이미지 링크 형식화
        photo_link = "https:" + photo['src']

        # 선수 포지션 태그 가져오기
        position = ""
        if soup.select_one('#cphContents_cphContents_cphContents_playerProfile_lblPosition') is not None:
            position = soup.select_one('#cphContents_cphContents_cphContents_playerProfile_lblPosition').text

        # 선수 스탯 출력
        if name is not None:
            print(rank, name,team,game, "AVG:", avg, "RUN:", run, "HIT:", hit, "HR:", hr, "RBI:", rbi,
                  "Link:", href, "Photo:", photo_link, "Position:", position)
            # 스탯 모으기
            data = {
                'Rank': rank,
                'Name': name,
                'Team': team,
                'Game': game,
                'Avg': avg,
                'Run': run,
                'Hit': hit,
                'Hr': hr,
                'RBI': rbi,
                'Link': href,
                'Photo': photo_link,
                'Position': position
            }

            # db에 입력하기
            collection.insert_one(data)
            rank += 1

# 각 KBO팀 2019년 선수 성적 크롤
crawler("두산")
crawler("롯데")
crawler("삼성")
crawler("키움")
crawler("한화")
crawler("KIA")
crawler("KT")
crawler("LG")
crawler("NC")
crawler("SK")


driver.close()
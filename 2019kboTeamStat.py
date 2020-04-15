from bs4 import BeautifulSoup
from selenium import webdriver
from pymongo import MongoClient

# pymongo를 임포트 하기
client = MongoClient('localhost', 27017)
# mongoDB는 27017 포트로 돌아갑니다.
db = client.testDB

# 드라이버 열기
driver = webdriver.Chrome('./chromedriver')

# KBO 2018년도 선수스탯 1페이지 크롤링

# URL 가져오기
driver.get('https://www.koreabaseball.com/Record/Team/Hitter/Basic1.aspx')

# 해당 페이지의 html 소스 선택
html = driver.page_source
# html 파싱하기
soup = BeautifulSoup(html, 'html.parser')
# tr 태그내용 가져오기
teams = soup.select('table.tData.tt > tbody > tr')

rank = 1
# tr 태그 내 선수 스탯 출력하기
for team in teams:
    name = team.find_all('td')[1].text # 이름
    avg = team.find('td', {'data-id': 'HRA_RT'}).text # 타율
    run = team.find('td', {'data-id': 'RUN_CN'}).text # 득점
    hit = team.find('td', {'data-id': 'HIT_CN'}).text # 안타
    hr = team.find('td', {'data-id': 'HR_CN'}).text # 홈런
    rbi = team.find('td', {'data-id': 'RBI_CN'}).text # 타점

    # 선수 스탯 출력
    if name is not None:
        print(rank, name, "AVG:", avg, "RUN:", run, "HIT:", hit, "HR:", hr, "RBI:", rbi)

        data = {
            'Rank': rank,
            'Name': name,
            'Avg': avg,
            'Run': run,
            'Hit': hit,
            'Hr': hr,
            'RBI': rbi
        }

        # db에 입력하기
        db.tyteamstat.insert_one(data)
        rank += 1


driver.close()

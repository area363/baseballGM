from bs4 import BeautifulSoup
from selenium import webdriver
import time
from pymongo import MongoClient

# pymongo를 임포트 하기
client = MongoClient('localhost', 27017)
# mongoDB는 27017 포트로 돌아갑니다.
db = client.testDB2

# 드라이버 열기
driver = webdriver.Chrome('./chromedriver')

# KBO 2018년도 선수스탯 크롤링 함수 (이 스탯을 기준으로 내 팀 선수를 선택한다)
def crawler2018(page, rank):
    # URL 가져오기
    driver.get('https://www.koreabaseball.com/Record/Player/HitterBasic/Basic1.aspx')
    # 스탯 옵션에서 2018년도 성적 선택하기
    driver.find_element_by_xpath("//select[@name='ctl00$ctl00$ctl00$cphContents$cphContents$cphContents$ddlSeason$ddlSeason']/option[text()='2018']").click()
    # 3초 스톱
    time.sleep(3)
    driver.find_element_by_xpath('//a[@href="'+"javascript:sort('GAME_CN');"+'"]').click()
    time.sleep(3)
    driver.find_element_by_id(f'cphContents_cphContents_cphContents_ucPager_btnNo{page}').click()
    time.sleep(3)
    # 해당 페이지의 html 소스 선택
    html = driver.page_source
    # html 파싱하기
    soup = BeautifulSoup(html, 'html.parser')
    # tr 태그내용 가져오기
    players = soup.select('div.record_result > table > tbody > tr')

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
            db.lyplayerstat.insert_one(data)
            rank += 1

# 50경기 이상 플레이한 선수 명단 크롤링
for x in range (1,6):
    crawler2018(x, (x-1)*30+1)

# KBO 2019년도 팀 당 선수스탯 크롤링 함수 (kbo 팀 성적 종합 용도)
def crawler2019(teams):
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

        # 팀 로고 가져오기
        team_logolink = ""
        if soup.select_one('span.emb > img') is not None:
            team_logo = soup.select_one('span.emb > img')
            team_logolink = "https:" + team_logo['src']

        # 선수 스탯 출력
        if name is not None:
            print(rank, name,team,game, "AVG:", avg, "RUN:", run, "HIT:", hit, "HR:", hr, "RBI:", rbi,
                  "Link:", href, "Photo:", photo_link, "Position:", position, "Logo:", team_logolink)
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
                'Position': position,
                'Logo': team_logolink
            }

            # db에 입력하기
            collection.insert_one(data)
            rank += 1

# 각 KBO팀 2019년 선수 성적 크롤
crawler2019("두산")
crawler2019("롯데")
crawler2019("삼성")
crawler2019("키움")
crawler2019("한화")
crawler2019("KIA")
crawler2019("KT")
crawler2019("LG")
crawler2019("NC")
crawler2019("SK")

# 2019년도 선수 전체 명단 가져오기1 (내 팀 선수 선택하기 용도)
def crawler20191(page, rank):
    # URL 가져오기
    driver.get('https://www.koreabaseball.com/Record/Player/HitterBasic/Basic1.aspx')
    # 3초 스톱
    time.sleep(3)
    driver.find_element_by_xpath('//a[@href="'+"javascript:sort('GAME_CN');"+'"]').click()
    time.sleep(3)
    driver.find_element_by_id(f'cphContents_cphContents_cphContents_ucPager_btnNo{page}').click()
    time.sleep(3)
    # 해당 페이지의 html 소스 선택
    html = driver.page_source
    # html 파싱하기
    soup = BeautifulSoup(html, 'html.parser')
    # tr 태그내용 가져오기
    players = soup.select('div.record_result > table > tbody > tr')

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
            db.typlayerstat.insert_one(data)
            rank += 1

# 2019년도 선수 전체 명단 가져오기2 (내 팀 선수 선택하기 용도)
def crawler20192(page, rank):
    # URL 가져오기
    driver.get('https://www.koreabaseball.com/Record/Player/HitterBasic/Basic1.aspx')
    # 3초 스톱
    time.sleep(3)
    driver.find_element_by_xpath('//a[@href="'+"javascript:sort('GAME_CN');"+'"]').click()
    time.sleep(3)
    driver.find_element_by_id('cphContents_cphContents_cphContents_ucPager_btnNext').click()
    time.sleep(3)
    driver.find_element_by_id(f'cphContents_cphContents_cphContents_ucPager_btnNo{page}').click()
    time.sleep(3)
    # 해당 페이지의 html 소스 선택
    html = driver.page_source
    # html 파싱하기
    soup = BeautifulSoup(html, 'html.parser')
    # tr 태그내용 가져오기
    players = soup.select('div.record_result > table > tbody > tr')

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
            db.typlayerstat.insert_one(data)
            rank += 1


# 50경기 이상 플레이한 선수 명단 크롤링
for x in range (1,6):
    crawler20191(x, (x-1)*30+1)

for x in range (1,6):
    crawler20192(x, (x+4)*30+1)

# 드라이버 닫기 
driver.close()

# 팀 별 컬렉션에서 최고 타자 8명의 성적을 종합해서 결과 컬렉션에 저장하기 
def calcTeamStat(team):
    
    players = list(db[team].find({}).limit(8))

    games = 0
    avg = 0
    run = 0
    hit = 0
    hr = 0
    rbi = 0
    logo = players[0]['Logo']

    for i in range(0, 8):
        games += int(players[i]['Game'])
        avg += float(players[i]['Avg'])
        run += int(players[i]['Run'])
        hit += int(players[i]['Hit'])
        hr += int(players[i]['Hr'])
        rbi += int(players[i]['RBI'])

    avg /= 8
    avg = "%.3f" % avg

    print(team, games, avg, run, hit, hr, rbi)

    data = {

        'Team': team,
        'Game': games,
        'Avg': avg,
        'Run': run,
        'Hit': hit,
        'Hr': hr,
        'RBI': rbi,
        'Logo': logo
    }

    # db에 입력하기
    db.vskbo.insert_one(data)


calcTeamStat("두산")
calcTeamStat("롯데")
calcTeamStat("삼성")
calcTeamStat("키움")
calcTeamStat("한화")
calcTeamStat("KIA")
calcTeamStat("KT")
calcTeamStat("LG")
calcTeamStat("NC")
calcTeamStat("SK")
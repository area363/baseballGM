from bs4 import BeautifulSoup
from selenium import webdriver
import time

# 드라이버 열기
driver = webdriver.Chrome('./chromedriver')

# KBO 2018년도 선수스탯 1페이지 크롤링

# URL 가져오기
driver.get('https://www.koreabaseball.com/Record/Player/HitterBasic/Basic1.aspx')
# 스탯 옵션에서 2018년도 성적 선택하기
driver.find_element_by_xpath("//select[@name='ctl00$ctl00$ctl00$cphContents$cphContents$cphContents$ddlSeason$ddlSeason']/option[text()='2018']").click()
# 1초 스톱
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
    a_tag = player.select_one('td > a') # 이름
    href = "https://www.koreabaseball.com" + a_tag['href'] # 선수 개별 페이지 링크
    avg = player.find('td', {'data-id': 'HRA_RT'}) # 타율
    run = player.find('td', {'data-id': 'RUN_CN'}) # 득점
    hit = player.find('td', {'data-id': 'HIT_CN'}) # 안타
    hr = player.find('td', {'data-id': 'HR_CN'}) # 홈런
    rbi = player.find('td', {'data-id': 'RBI_CN'}) # 타점

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

    # 선수 스탯 출력
    if a_tag is not None:
        print(rank, a_tag.text, "AVG:", avg.text, "RUN:", run.text, "HIT:", hit.text, "HR:", hr.text, "RBI:", rbi.text,
              "Link:", href, "Photo:", photo_link)
        rank += 1

# KBO 2018년도 선수스탯 2페이지 크롤링 (위와 동일한 형식)

driver.get('https://www.koreabaseball.com/Record/Player/HitterBasic/Basic1.aspx')
driver.find_element_by_xpath("//select[@name='ctl00$ctl00$ctl00$cphContents$cphContents$cphContents$ddlSeason$ddlSeason']/option[text()='2018']").click()
time.sleep(1)
driver.find_element_by_id('cphContents_cphContents_cphContents_ucPager_btnNo2').click()
time.sleep(1)

html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

players = soup.select('div.record_result > table > tbody > tr')

for player in players:
    a_tag = player.select_one('td > a')
    href = "https://www.koreabaseball.com" + a_tag['href']
    avg = player.find('td', {'data-id': 'HRA_RT'})
    run = player.find('td', {'data-id': 'RUN_CN'})
    hit = player.find('td', {'data-id': 'HIT_CN'})
    hr = player.find('td', {'data-id': 'HR_CN'})
    rbi = player.find('td', {'data-id': 'RBI_CN'})
    driver.get(href)

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')
    photo = soup.select_one('div.photo > img')
    photo_link = "https:" + photo['src']

    if a_tag is not None:
        print(rank, a_tag.text, "AVG:", avg.text, "RUN:", run.text, "HIT:", hit.text, "HR:", hr.text, "RBI:", rbi.text,
              "Link:", href, "Photo:", photo_link)
        rank += 1

# KBO 2018년도 선수스탯 3페이지 크롤링 (위와 동일한 형식)

driver.get('https://www.koreabaseball.com/Record/Player/HitterBasic/Basic1.aspx')
driver.find_element_by_xpath("//select[@name='ctl00$ctl00$ctl00$cphContents$cphContents$cphContents$ddlSeason$ddlSeason']/option[text()='2018']").click()
time.sleep(1)
driver.find_element_by_id('cphContents_cphContents_cphContents_ucPager_btnNo3').click()
time.sleep(1)

html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

players = soup.select('div.record_result > table > tbody > tr')

for player in players:
    a_tag = player.select_one('td > a')
    href = "https://www.koreabaseball.com" + a_tag['href']
    avg = player.find('td', {'data-id': 'HRA_RT'})
    run = player.find('td', {'data-id': 'RUN_CN'})
    hit = player.find('td', {'data-id': 'HIT_CN'})
    hr = player.find('td', {'data-id': 'HR_CN'})
    rbi = player.find('td', {'data-id': 'RBI_CN'})

    driver.get(href)

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')
    photo = soup.select_one('div.photo > img')
    photo_link = "https:" + photo['src']

    if a_tag is not None:
        print(rank, a_tag.text, "AVG:", avg.text, "RUN:", run.text, "HIT:", hit.text, "HR:", hr.text, "RBI:", rbi.text,
              "Link:", href, "Photo:", photo_link)
        rank += 1

driver.close()

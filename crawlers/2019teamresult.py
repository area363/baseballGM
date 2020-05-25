from pymongo import MongoClient

# pymongo를 임포트 하기
client = MongoClient('localhost', 27017)
# mongoDB는 27017 포트로 돌아갑니다.
db = client.testDB

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


calcTeamStat("Doosan Bears")
calcTeamStat("Lotte Giants")
calcTeamStat("Samsung Lions")
calcTeamStat("Kiwoom Heroes")
calcTeamStat("Hanwha Eagles")
calcTeamStat("KIA Tigers")
calcTeamStat("KT Wiz")
calcTeamStat("LG Twins")
calcTeamStat("NC Dinos")
calcTeamStat("SK Wyverns")



from pymongo import MongoClient

# pymongo를 임포트 하기
client = MongoClient('localhost', 27017)
# mongoDB는 27017 포트로 돌아갑니다.
db = client.testDB

teams = list(db.vskbo.find({}, {"_id" : 0}).sort('rank',-1))

print(teams)

# db.vskbo.delete_one({"Team": "스파르타"})

# def calcTeamStat(teams):

#     team = teams
#     # players = list(db[team].find({ 'Rank': { '$lt': 9 } }, {'_id' : 0}))
#     players = list(db[team].find({}).limit(8))


#     games = 0
#     avg = 0
#     run = 0
#     hit = 0
#     hr = 0
#     rbi = 0

#     for i in range(0, 8):
#         games += int(players[i]['Game'])
#         avg += float(players[i]['Avg'])
#         run += int(players[i]['Run'])
#         hit += int(players[i]['Hit'])
#         hr += int(players[i]['Hr'])
#         rbi += int(players[i]['RBI'])

#     avg /= 8
#     avg = "%.3f" % avg

#     print(team, games, avg, run, hit, hr, rbi)

#     data = {

#         'Team': team,
#         'Game': games,
#         'Avg': avg,
#         'Run': run,
#         'Hit': hit,
#         'Hr': hr,
#         'RBI': rbi,
#     }

#     # db에 입력하기
#     db.vskbo.insert_one(data)


# calcTeamStat("두산")
# calcTeamStat("롯데")
# calcTeamStat("삼성")
# calcTeamStat("키움")
# calcTeamStat("한화")
# calcTeamStat("KIA")
# calcTeamStat("KT")
# calcTeamStat("LG")
# calcTeamStat("NC")
# calcTeamStat("SK")


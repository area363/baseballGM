from pymongo import MongoClient

# pymongo를 임포트 하기
client = MongoClient('localhost', 27017)
# mongoDB는 27017 포트로 돌아갑니다.
db = client.testDB2


db["두산"].drop()
db["롯데"].drop()
db["삼성"].drop()
db["키움"].drop()
db["한화"].drop()
db["KIA"].drop()
db["KT"].drop()
db["LG"].drop()
db["NC"].drop()
db["SK"].drop()
db.lyplayerstat.drop()
db.typlayerstat.drop()
db.vskbo.drop()
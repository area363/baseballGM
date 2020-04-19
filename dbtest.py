
from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

client = MongoClient('localhost', 27017)
db = client.testDB

# API 역할을 하는 부분
# @app.route('/api/list', methods=['GET'])
# def player_list():
    # 1. mystar 목록 전체를 검색합니다. ID는 제외하고 like 가 많은 순으로 정렬합니다.
    # 참고) find({},{'_id':False}), sort()를 활용하면 굿!
    # 2. 성공하면 success 메시지와 함께 stars_list 목록을 클라이언트에 전달합니다.

players = list(db.lyplayerstat.find({}, {"_id" : 0}).sort('rank',-1))

print({'result': 'success','msg':'list 연결되었습니다!', 'data' : players})
# -*- coding: utf-8 -*-
from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.testDB

@app.route('/')
def welcome():
    return render_template("index.html")

@app.route('/selectmyteam')
def my_team():
    return render_template("selectmyteam.html")

@app.route('/viewmyteam')
def view_my_team():
    return render_template("viewmyteam.html")

@app.route('/vskbo')
def vs_kbo():
    return render_template("vskbo.html")

# API 역할을 하는 부분
@app.route('/api/list', methods=['GET'])
def player_list():
    # 1. mystar 목록 전체를 검색합니다. ID는 제외하고 like 가 많은 순으로 정렬합니다.
    # 참고) find({},{'_id':False}), sort()를 활용하면 굿!
    # 2. 성공하면 success 메시지와 함께 stars_list 목록을 클라이언트에 전달합니다.

    players = list(db.lyplayerstat.find({}, {"_id" : 0}).sort('rank',-1))
    return jsonify({'result': 'success','msg':'list 연결되었습니다!', 'data' : players})

@app.route('/api/check', methods=['POST'])
def player_number():

    client_id = request.form['clientid']
    if db[client_id].count_documents({}) < 8:
        return jsonify({'result': 'lessthan8'})
    else:
        return jsonify({'result': 'success'})

@app.route('/api/pick', methods=['POST'])
def player_pick():
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    name_receive = request.form['name_give']
    client_id = request.form['clientid']

    if db[client_id].count_documents({}) > 7:
        return jsonify({'result': 'morethan8'})

    # 2. mystar 목록에서 find_one으로 name이 name_receive와 일치하는 star를 찾습니다.
    if db.typlayerstat.count_documents({ 'Name':name_receive }, limit = 1) == 0:
        return jsonify({'result': 'DNE'})
    else:
        player = db.typlayerstat.find_one({'Name':name_receive})

    
    if db[client_id].count_documents({ 'Name':name_receive }, limit = 1) != 0:
        return jsonify({'result': 'fail'})
    else:
        db[client_id].insert_one(player)

    count = db[client_id].count_documents({})

    # 5. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success', 'count': count})

@app.route('/api/delete', methods=['POST'])
def player_delete():
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    name_receive = request.form['name_give']
    client_id = request.form['clientid']
    if db[client_id].count_documents({ 'Name':name_receive }, limit = 1) == 0:
        return jsonify({'result': 'DNE'})
    else:
        db[client_id].remove({'Name':name_receive})
        count = db[client_id].count_documents({})
        return jsonify({'result': 'success', 'count': count})

@app.route('/api/deleteall', methods=['POST'])
def players_delete():
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    client_id = request.form['id']
    db.vskbo.delete_one({"Team": "사용자ID: " + client_id})
    return jsonify({'result': 'success'})

@app.route('/api/finalteam', methods=['POST'])
def team_final():
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.

    client_id = request.form['id']
    players = list(db[client_id].find({}))


    games = 0
    avg = 0
    run = 0
    hit = 0
    hr = 0
    rbi = 0
    logo = "https://image.rocketpunch.com/company/103338/spartacodingclub_logo_1584940180.jpg?s=400x400&t=inside"

    for i in range(0, 8):
        games += int(players[i]['Game'])
        avg += float(players[i]['Avg'])
        run += int(players[i]['Run'])
        hit += int(players[i]['Hit'])
        hr += int(players[i]['Hr'])
        rbi += int(players[i]['RBI'])

    avg /= 8
    avg = "%.3f" % avg

    data = {

        'Team': "사용자ID: " + client_id,
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
    return jsonify({'result': 'success'})

@app.route('/api/myteamlist', methods=['POST'])
def myplayer_list():
    # 1. mystar 목록 전체를 검색합니다. ID는 제외하고 like 가 많은 순으로 정렬합니다.
    # 참고) find({},{'_id':False}), sort()를 활용하면 굿!
    # 2. 성공하면 success 메시지와 함께 stars_list 목록을 클라이언트에 전달합니다.
    client_id = request.form['id']
    players = list(db[client_id].find({}, {"_id" : 0}).sort('rank',-1))
    return jsonify({'result': 'success','msg':'list 연결되었습니다!', 'data' : players})

@app.route('/api/result', methods=['GET'])
def result_list():
    # 1. mystar 목록 전체를 검색합니다. ID는 제외하고 like 가 많은 순으로 정렬합니다.
    # 참고) find({},{'_id':False}), sort()를 활용하면 굿!
    # 2. 성공하면 success 메시지와 함께 stars_list 목록을 클라이언트에 전달합니다.

    teams = list(db.vskbo.find({}, {"_id" : 0}).sort('rank',-1))
    return jsonify({'result': 'success','msg':'list 연결되었습니다!', 'data' : teams})

if __name__ == "__main__":
    app.run('0.0.0.0', port = 5000, debug = True)


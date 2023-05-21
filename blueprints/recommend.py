from flask import Blueprint, request
import json
from operator import itemgetter
from models.cam import Cam
from exts import db as datebase

db = Blueprint("recommend", __name__, url_prefix='/user')


def recommend(user):
    print(user)
    K = 20
    N = 10
    rank = {}
    with open('C:\\Users\\86176\\Desktop\\openCams\\OpenCamsUserSide\\dataSet.json', mode='r+') as f:
        trainSet = json.loads(f.read())
    with open('C:\\Users\\86176\\Desktop\\openCams\\OpenCamsUserSide\\SimMatrix.json', mode='r+') as f:
        user_sim_matrix = json.loads(f.read())
    watched_movies = trainSet[user]
    for v, wuv in sorted(user_sim_matrix[user].items(), key=itemgetter(1), reverse=True)[0:K]:
        movies = trainSet[v]
        for movie in trainSet[v]:
            if movie in watched_movies:
                continue
            rank.setdefault(movie, 0)
            rank[movie] += wuv * float(movies[movie])
    return sorted(rank.items(), key=itemgetter(1), reverse=True)[0:N]

@db.route('/recommend', methods=['GET'])
def queryRecommend():
    data = request.args
    id = data.get('id')
    ids = recommend(id)
    currIds = []
    for item in ids:
        currIds.append(int(item[0]))
    rec = Cam.query.filter(Cam.id.in_(currIds)).order_by(Cam.score.desc()).all()
    res = []
    for i in rec:
        res.append(i.to_json())
    return {
        "errno": 0,
        "errmsg": '',
        "data": res
    }
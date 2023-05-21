from flask import Blueprint, request
import json
from operator import itemgetter
from sqlalchemy import and_
from models.cam import Cam
from models.operation import Like, DisLike, Collect, Visit
from exts import db as datebase

db = Blueprint("camdetail", __name__, url_prefix='/user')


def recommend(user):
    K = 20
    rank = {}
    with open('C:\\Users\\86176\\Desktop\\openCams\\OpenCamsUserSide\\dataSetICF.json', mode='r+') as f:
        trainSet = json.loads(f.read())
    with open('C:\\Users\\86176\\Desktop\\openCams\\OpenCamsUserSide\\SimMatrixICF.json', mode='r+') as f:
        movie_sim_matrix = json.loads(f.read())
    watched_movies = trainSet[user]
    for movie, rating in watched_movies.items():
        for related_movie, w in sorted(movie_sim_matrix[movie].items(), key=itemgetter(1), reverse=True)[:K]:
            if related_movie in watched_movies:
                continue
            rank.setdefault(related_movie, 0)
            rank[related_movie] += w * float(rating)
    return sorted(rank.items(), key=itemgetter(1), reverse=True)

@db.route('/cam', methods=['GET'])
def queryCams():
    data = request.args
    id = data.get('id')
    uid = data.get('uid')
    cam = Cam.query.filter(Cam.id == id).first()
    like = Like.query.filter(
        and_(id == Like.cid),
        and_(uid == Like.uid)
    ).first()
    likenum = Like.query.filter(
        and_(id == Like.cid),
        and_(uid == Like.uid)
    ).count()

    dislike = DisLike.query.filter(
        and_(id == DisLike.cid),
        and_(uid == DisLike.uid)
    ).first()

    dislikenum = DisLike.query.filter(
        and_(id == DisLike.cid),
        and_(uid == DisLike.uid)
    ).count()

    collect = Collect.query.filter(
        and_(id == Collect.cid),
        and_(uid == Collect.uid)
    ).first()
    collectnum = Collect.query.filter(
        and_(id == Collect.cid),
        and_(uid == Collect.uid)
    ).count()
    isLike = False
    isDisLike = False
    isCollect = False
    if like != None:
        isLike = True
    if collect != None:
        isCollect = True
    if dislike != None:
        isDisLike = True
    ids = recommend(uid)
    currIds = []
    for item in ids:
        currIds.append(int(item[0]))
    rec = Cam.query.filter(Cam.id.in_(currIds), Cam.mainTag == cam.mainTag, Cam.id != cam.id).order_by(Cam.score.desc()).limit(10).all()
    res = []
    for i in rec:
        res.append(i.to_json())
    return {
        "errno": 0,
        "errmsg": '',
        "data":{
            "data": cam.to_json1(isLike, isDisLike, isCollect, likenum, dislikenum, collectnum),
            "recommend": res
        }
    }

@db.route('/setlike', methods=['POST'])
def setLike():
    data = request.get_json()
    uid = data.get('uid')
    cid = data.get('cid')
    like = data.get('like')
    res = Like.query.filter(
        and_(cid == Like.cid),
        and_(uid == Like.uid)
    ).first()
    cam = Cam.query.filter(Cam.id == cid).first()
    if res == None and like == True:
        l = Like(cid = cid, uid = uid)
        datebase.session.add(l)
        dislike = DisLike.query.filter(
            and_(cid == DisLike.cid),
            and_(uid == DisLike.uid)
        ).first()
        cam.like = cam.like + 1
        cam.score = cam.score + 10
        if dislike != None:
            DisLike.query.filter(
                and_(cid == DisLike.cid),
                and_(uid == DisLike.uid)
            ).delete()
            cam.dislike = cam.dislike - 1
            cam.score = cam.score + 10
        datebase.session.commit()
    elif res != None and like == False:
        Like.query.filter(
            and_(cid == Like.cid),
            and_(uid == Like.uid)
        ).delete()
        cam.like = cam.like - 1
        cam.score = cam.score - 10
        datebase.session.commit()
    else:
        return {
            "errno": 1,
            "errmsg": '参数错误',
        }
    return {
        "errno": 0,
        "errmsg": '',
    }

@db.route('/setdislike', methods=['POST'])
def setDisLike():
    data = request.get_json()
    uid = data.get('uid')
    cid = data.get('cid')
    disLike = data.get('disLike')
    res = DisLike.query.filter(
        and_(cid == DisLike.cid),
        and_(uid == DisLike.uid)
    ).first()
    cam = Cam.query.filter(Cam.id == cid).first()
    if res == None and disLike == True:
        l = DisLike(cid = cid, uid = uid)
        datebase.session.add(l)
        like = Like.query.filter(
            and_(cid == Like.cid),
            and_(uid == Like.uid)
        ).first()
        cam.dislike = cam.dislike + 1
        cam.score = cam.score - 10
        if like != None:
            Like.query.filter(
                and_(cid == Like.cid),
                and_(uid == Like.uid)
            ).delete()
            cam.like = cam.like - 1
            cam.score = cam.score - 10
        datebase.session.commit()
    elif res != None and disLike == False:
        DisLike.query.filter(
            and_(cid == DisLike.cid),
            and_(uid == DisLike.uid)
        ).delete()
        cam.dislike = cam.dislike - 1
        cam.score = cam.score + 10
        datebase.session.commit()
    else:
        return {
            "errno": 1,
            "errmsg": '参数错误',
        }
    return {
        "errno": 0,
        "errmsg": '',
    }

@db.route('/setcollect', methods=['POST'])
def setCollect():
    data = request.get_json()
    uid = data.get('uid')
    cid = data.get('cid')
    collect = data.get('collect')
    res = Collect.query.filter(
        and_(cid == Collect.cid),
        and_(uid == Collect.uid)
    ).first()
    if res == None and collect == True:
        l = Collect(cid = cid, uid = uid)
        datebase.session.add(l)
        datebase.session.commit()
    elif res != None and collect == False:
        DisLike.query.filter(
            and_(cid == DisLike.cid),
            and_(uid == DisLike.uid)
        ).delete()
        datebase.session.commit()
    else:
        return {
            "errno": 1,
            "errmsg": '参数错误',
        }
    return {
        "errno": 0,
        "errmsg": '',
    }

@db.route('/clickcam', methods=['POST'])
def clickCam():
    data = request.get_json()
    uid = data.get('uid')
    cid = data.get('cid')
    visit = Visit(uid=uid, cid=cid)
    datebase.session.add(visit)
    cam = Cam.query.filter(Cam.id == cid).first()
    cam.clickcount = cam.clickcount + 1
    cam.score = cam.score + 1
    datebase.session.commit()
    return {
        "errno": 0,
        "errmsg": '',
    }
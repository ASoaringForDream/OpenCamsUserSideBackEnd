from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from models.cam import Cam, CamMainTag, CamTag



db = Blueprint("cam", __name__, url_prefix='/user')

@db.route('/cams', methods=['GET'])
def queryCams():
    data = request.args
    search = data.get('search')
    mainTag = data.get('mainTag')
    tag = data.get('tag')
    city = data.get('city')
    country = data.get('country')
    state = data.get('state')
    current = int(data.get('current'))
    pageSize = int(data.get('pageSize'))
    allCams = Cam.query.filter(
        or_(Cam.city == city, city == None, city == ''),
        or_(Cam.country == country, country == None, country == ''),
        or_(Cam.state == state, state == None, state == ''),
        or_(search == None, Cam.desc.like('%' + str(search) + '%'), search == ''),
        or_(tag == None, Cam.tag == tag, Cam.tag.like(str(tag) + ',%'), Cam.tag.like('%,' + str(tag) + ',%'), Cam.tag.like('%,' + str(tag)), tag == ''),
        or_(Cam.mainTag == mainTag, mainTag == None, mainTag == '')).all()
    cams = Cam.query.filter(
        or_(Cam.city == city, city == None, city == ''),
        or_(Cam.country == country, country == None, country == ''),
        or_(Cam.state == state, state == None, state == ''),
        or_(search == None, Cam.desc.like('%' + str(search) + '%'), search == ''),
        or_(tag == None, Cam.tag == tag, Cam.tag.like(str(tag) + ',%'), Cam.tag.like('%,' + str(tag) + ',%'), Cam.tag.like('%,' + str(tag)), tag == ''),
        or_(Cam.mainTag == mainTag, mainTag == None, mainTag == '')).order_by(Cam.score.desc()).offset((current - 1) * pageSize).limit(pageSize).all()
    res = []
    for item in cams:
        res.append(item.to_json())
    return {
        "errno": 0,
        "errmsg": '',
        "data":{
            "total": len(allCams),
            "data": res
        }
    }

@db.route('/swiper', methods=['GET'])
def querySwiper():
    cams = Cam.query.order_by(Cam.score.desc()).limit(5).all()
    res = []
    for item in cams:
        res.append(item.to_json())
    return {
        "errno": 0,
        "errmsg": '',
        "data":{
            "data": res
        }
    }

@db.route('/camTags', methods=['GET'])
def querycamtags():
    camMainTags = CamMainTag.query.all()
    camTags = CamTag.query.all()
    main = []
    for item in camMainTags:
        main.append(item.to_json())
    tag = []
    for item in camTags:
        tag.append(item.to_json())
    return {
        "errno": 0,
        "errmsg": '',
        "data": {
            "data": main,
            "tags": tag
        }
    }
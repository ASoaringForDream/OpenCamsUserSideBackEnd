from flask import Blueprint, request
import datetime
from models.cam import Cam
from models.operation import Like, DisLike, Collect, Visit

db = Blueprint("personal", __name__, url_prefix='/user')

@db.route('/querycollect', methods=['GET'])
def queryCollect():
    data = request.args
    id = data.get('id')
    current = int(data.get('current'))
    pageSize = int(data.get('pageSize'))
    all = Collect.query.filter(id == Collect.uid).count()
    collects = Collect.query.filter(id == Collect.uid).offset((current - 1) * pageSize).limit(pageSize).all()
    res = []
    for item in collects:
        res.append(item.to_json())
    return  {
        "errno": 0,
        "errmsg": '',
        "data": {
            "total": all,
            "data": res
        }
    }

@db.route('/queryhistory', methods=['GET'])
def queryHistory():
    data = request.args
    id = data.get('id')
    current = int(data.get('current'))
    pageSize = int(data.get('pageSize'))
    all = Visit.query.filter(id == Visit.uid).count()
    time = datetime.timedelta(days=15)
    d = datetime.datetime.now() -time
    visits = Visit.query.filter(id == Visit.uid, Visit.visittime > d).order_by(Visit.visittime.desc()).offset((current - 1) * pageSize).limit(pageSize).all()
    # datetime.timedelta.days
    res = []
    for item in visits:
        res.append(item.to_json())
    return  {
        "errno": 0,
        "errmsg": '',
        "data": {
            "total": all,
            "data": res
        }
    }
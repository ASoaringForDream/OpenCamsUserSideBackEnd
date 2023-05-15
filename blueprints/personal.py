from flask import Blueprint, request
import datetime
from sqlalchemy import func
from models.cam import Cam
from models.operation import Like, DisLike, Collect, Visit
from exts import db as datebase

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
    time = datetime.timedelta(days=15)
    d = datetime.datetime.now() - time
    all = datebase.session.query(Visit.cid, Visit.uid, func.max(Visit.visittime)).filter(id == Visit.uid, Visit.visittime > d).group_by(Visit.cid).count()
    visits = datebase.session.query(Visit.cid, Visit.uid, func.max(Visit.visittime), Cam).join(Cam, Visit.cid == Cam.id).filter(id == Visit.uid, Visit.visittime > d).group_by(Visit.cid).order_by(func.max(Visit.visittime).desc()).offset((current - 1) * pageSize).limit(pageSize).all()
    print(visits)
    res = []
    for item in visits:
        res.append({
            "cid": item[0],
            "uid": item[1],
            "visittime": item[2],
            "cam": item[3].to_json()
        })
    return  {
        "errno": 0,
        "errmsg": '',
        "data": {
            "total": all,
            "data": res
        }
    }
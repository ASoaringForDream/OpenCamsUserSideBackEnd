from flask import Blueprint, request
from sqlalchemy import and_
from models.cam import Cam

db = Blueprint("camdetail", __name__, url_prefix='/user')

@db.route('/cam', methods=['GET'])
def queryCams():
    data = request.args
    id = data.get('id')
    cam = Cam.query.filter(Cam.id == id).first()
    mainTag = cam.mainTag
    recommend = Cam.query.filter(
        and_(Cam.mainTag == mainTag),
        and_(Cam.id != id)
    ).order_by(Cam.score.desc()).limit(10).all()
    res = []
    for item in recommend:
        res.append(item.to_json())
    return {
        "errno": 0,
        "errmsg": '',
        "data":{
            "data": cam.to_json(),
            "recommend": res
        }
    }
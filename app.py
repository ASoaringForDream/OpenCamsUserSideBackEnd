from flask import Flask
import datetime
from config import DevelopmentConfig
from exts import config_extensions
from blueprints import config_blueprint
from flask_cors import CORS
from models.cam import Cam
from models.user import User
from models.operation import Visit, Like, DisLike, Collect
from exts import db as datebase
import random

app = Flask(__name__)
CORS(app, supports_credentials=True, origins='http://localhost:7001')

app.config.from_object(DevelopmentConfig)
config_extensions(app)
config_blueprint(app)

@app.route('/')
def print_hi():
    users = User.query.all()
    cams = Cam.query.all()
    res = []
    for item in users:
        allVisit = datebase.session.query(Visit.cid).filter(item.id == Visit.uid).group_by(Visit.cid).all()
        # print(allVisit)
        for i in allVisit:
            cid = i[0]
            visits = Visit.query.filter(item.id == Visit.uid).all()
            dislike = DisLike.query.filter(item.id == DisLike.uid, cid == DisLike.cid).all()
            like = Like.query.filter(item.id == DisLike.uid, cid == DisLike.cid).all()
            collect = Collect.query.filter(item.id == Collect.uid, cid == Collect.cid).all()
            count = len(visits) - 10 * len(dislike) + 10 * len(like) + 100 * len(collect)
            string = str(item.id) + ',' + str(cid) + ',' + str(count) + '\n'
            res.append(string)
    with open(f'C:\\Users\\86176\\Desktop\\openCams\\OpenCamsUserSide\\{str(datetime.datetime.now()).replace(" ", "-").replace(":", "-").split(".")[0]}.csv', mode='w') as file:
        file.writelines(res)
    return str(datetime.datetime.now()).replace(' ', '-')


if __name__ == '__main__':
    app.run(debug=True, port=5000)

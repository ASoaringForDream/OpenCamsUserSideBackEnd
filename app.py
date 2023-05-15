from flask import Flask
from config import DevelopmentConfig
from exts import config_extensions
from blueprints import config_blueprint
from flask_cors import CORS
from models.cam import Cam
from exts import db as datebase

app = Flask(__name__)
CORS(app, supports_credentials=True, origins='http://localhost:7001')

app.config.from_object(DevelopmentConfig)
config_extensions(app)
config_blueprint(app)

@app.route('/')
def print_hi():
    cams = Cam.query.all()
    for item in cams:
        print(item.score)
        if item.score == None:
            item.score = 0
    datebase.session.commit()
if __name__ == '__main__':
    app.run(debug=True, port=5000)

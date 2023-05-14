from flask import Flask
from config import DevelopmentConfig
from exts import config_extensions
from blueprints import config_blueprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True, origins='http://localhost:7001')

app.config.from_object(DevelopmentConfig)
config_extensions(app)
config_blueprint(app)

@app.route('/')
def print_hi():
    return "hello world"

if __name__ == '__main__':
    app.run(debug=True, port=5000)

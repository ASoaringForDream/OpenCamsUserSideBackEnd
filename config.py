HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD = "root"
DATABASE = "open_cams"

class Config:
    # 秘钥
    SECRET_KEY = 'openCams'

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8"
    SECRET_KEY = 'openCamsUserSide'
    SESSION_COOKIE_SAMESITE = 'None'
    SESSION_COOKIE_SECURE = True
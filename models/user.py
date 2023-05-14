import datetime
from exts import db
from sqlalchemy.dialects.mysql import LONGTEXT

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    creattime = db.Column(db.DateTime, default=datetime.datetime.now)
    name = db.Column(db.String(12))
    sex = db.Column(db.Enum("男","女","保密"), nullable=False, default="保密")
    state = db.Column(db.Enum("正常", "封禁"), nullable=False, default="正常")
    birth = db.Column(db.Date, default=datetime.date.today)
    telephone = db.Column(db.String(20))
    mailbox = db.Column(db.String(32), nullable=False)
    userpic = db.Column(LONGTEXT)

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "creattime": self.creattime,
            "name": self.name,
            "sex": self.sex,
            "state": self.state,
            "birth": self.birth,
            "telephone": self.telephone,
            "mailbox": self.mailbox,
            "userpic": self.userpic
        }
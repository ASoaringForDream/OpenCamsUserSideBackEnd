import datetime, time
from flask import jsonify
from sqlalchemy.dialects.mysql import LONGTEXT
from exts import db


class Manager(db.Model):
    __tablename__ = "manager"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    role = db.Column(db.Integer, db.ForeignKey("role.id"), nullable=False)
    creattime = db.Column(db.DateTime, default=datetime.datetime.now)
    name = db.Column(db.String(12), nullable=False)
    sex = db.Column(db.Enum("男","女","保密"), nullable=False, default="保密")
    birth = db.Column(db.Date, default = datetime.date.today)
    telephone = db.Column(db.String(20))
    mailbox = db.Column(db.String(32), nullable=False, unique=True)
    userpic = db.Column(LONGTEXT)

    role_ids = db.relationship("Role")

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,
            "creattime": self.creattime,
            "name": self.name,
            "sex": self.sex,
            "birth": self.birth,
            "telephone": self.telephone,
            "mailbox": self.mailbox,
            "userpic": self.userpic,
            "role_ids": self.role_ids.to_json()
        }
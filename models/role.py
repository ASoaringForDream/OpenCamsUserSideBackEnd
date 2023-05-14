from exts import db
from flask import jsonify

class Roleitem(db.Model):
    __tablename__ = "role_item"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
        }

class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    role_ids = db.Column(db.String(64), nullable=False)
    role_desc = db.Column(db.Text)

    def to_json(self):
        role_ids = self.role_ids.split(',')
        role_ids_int = []
        for item in role_ids:
            role_ids_int.append(int(item))
        return {
            "id": self.id,
            "name": self.name,
            "role_ids": role_ids_int,
            "role_desc": self.role_desc
        }
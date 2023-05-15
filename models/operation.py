import datetime
from exts import db

class Like(db.Model):
    __tablename__ = "likeed"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    cid = db.Column(db.Integer, db.ForeignKey("cam.id"), nullable=False)
    creattime = db.Column(db.DateTime, default=datetime.datetime.now)

class DisLike(db.Model):
    __tablename__ = "dislikeed"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    cid = db.Column(db.Integer, db.ForeignKey("cam.id"), nullable=False)
    creattime = db.Column(db.DateTime, default=datetime.datetime.now)

class Visit(db.Model):
    __tablename__ = "visit"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    cid = db.Column(db.Integer, db.ForeignKey("cam.id"), nullable=False)
    visittime = db.Column(db.DateTime, default=datetime.datetime.now)

    cam = db.relationship("Cam")

    def to_json(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "cid": self.cid,
            "visittime": self.visittime,
            "cam": self.cam.to_json()
        }

class Collect(db.Model):
    __tablename__ = "collect"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    cid = db.Column(db.Integer, db.ForeignKey("cam.id"), nullable=False)
    collecttime = db.Column(db.DateTime, default=datetime.datetime.now)

    cam = db.relationship("Cam")

    def to_json(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "cid": self.cid,
            "collecttime": self.collecttime,
            "cam": self.cam.to_json()
        }
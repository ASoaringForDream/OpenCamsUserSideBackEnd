from exts import db

class Cam(db.Model):
    __tablename__ = "cam"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tit = db.Column(db.Text, nullable=False)
    source = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    origin = db.Column(db.Text, nullable=False)
    originId = db.Column(db.String(256))
    like = db.Column(db.Integer, default=0, nullable=False)
    dislike = db.Column(db.Integer, default=0, nullable=False)
    clickcount = db.Column(db.Integer, default=0, nullable=False)
    type = db.Column(db.Enum("iframe", "HLS"), nullable=False)
    tag = db.Column(db.Text)
    mainTag = db.Column(db.Integer)
    posterImgPath = db.Column(db.String(512))
    posterImg = db.Column(db.String(256))
    country = db.Column(db.String(256))
    state = db.Column(db.String(256))
    city = db.Column(db.String(256))
    score = db.Column(db.Integer, default=0)

    def to_json(self):
        tag_int = []
        if self.tag != None and self.tag != '':
            tag = self.tag.split(',')
            for item in tag:
                tag_int.append(int(item))

        return {
            "id": self.id,
            "tit": self.tit,
            "source": self.source,
            "desc": self.desc,
            "origin": self.origin,
            "like": self.like,
            "dislike": self.dislike,
            "clickcount": self.clickcount,
            "type": self.type,
            "tag": tag_int,
            "mainTag": self.mainTag,
            "posterImg": self.posterImg,
            "country": self.country,
            "state": self.state,
            "city": self.city
        }

class CamMainTag(db.Model):
    __tablename__ = "cam_main_tag"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
        }

class CamTag(db.Model):
    __tablename__ = "cam_tag"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
        }
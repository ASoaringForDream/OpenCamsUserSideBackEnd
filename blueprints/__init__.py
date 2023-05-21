from .auth import db as auth
from .home import db as home
from  .cam import db as cam
from  .personal import db as personal
from .recommend import db as recommend

DEFAULT_BLUEPRINT = [auth, home, cam, personal, recommend]

def config_blueprint(app):
    for blueprint in DEFAULT_BLUEPRINT:
        app.register_blueprint(blueprint)
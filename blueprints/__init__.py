from .auth import db as auth
from .home import db as home
from  .cam import db as cam

DEFAULT_BLUEPRINT = [auth, home, cam]

def config_blueprint(app):
    for blueprint in DEFAULT_BLUEPRINT:
        app.register_blueprint(blueprint)
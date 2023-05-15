from .auth import db as auth
from .home import db as home
from  .cam import db as cam
from  .personal import db as personal

DEFAULT_BLUEPRINT = [auth, home, cam, personal]

def config_blueprint(app):
    for blueprint in DEFAULT_BLUEPRINT:
        app.register_blueprint(blueprint)
from .auth import db as auth
from .home import db as home

DEFAULT_BLUEPRINT = [auth, home]

def config_blueprint(app):
    for blueprint in DEFAULT_BLUEPRINT:
        app.register_blueprint(blueprint)
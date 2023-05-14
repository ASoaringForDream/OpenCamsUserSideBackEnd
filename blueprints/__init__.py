from .auth import db as auth

DEFAULT_BLUEPRINT = [auth]

def config_blueprint(app):
    for blueprint in DEFAULT_BLUEPRINT:
        app.register_blueprint(blueprint)
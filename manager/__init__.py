from flask import Flask, request
from flask_login import current_user, login_required
from itsdangerous import URLSafeTimedSerializer
from manager.models import *
from manager.ext import csrf, db, login_manager, dbt, mail

def create_app(config=None):

    app = Flask(__name__, instance_relative_config=True,
                          static_folder='../public/static',
                          template_folder='../public/templates')

    app.config.from_object('config.settings.DevConfig')

    if config:
        app.config.update(config)

    with app.app_context():
        extensions(app)
        register_apps(app)
        authentication(app, User)

    return app


def extensions(app):    
    csrf.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    dbt.init_app(app)
    login_manager.init_app(app)

    return None

def register_apps(app):
    from manager.apps import main, users, customers, billing, inventory
    from manager.apps import calls
    
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(customers)
    app.register_blueprint(inventory)
    app.register_blueprint(billing)
    app.register_blueprint(calls)
    # app.register_blueprint(stripe_webhook)

    return None


def authentication(app, user_model):
    login_manager.login_view = 'users.login'

    @login_manager.user_loader
    def load_user(uid):
        return user_model.query.get(uid)

# def template_processors(app):
#     """
#     Register 0 or more custom template processors (mutates the app passed in).

#     :param app: Flask application instance
#     :return: App jinja environment
#     """
#     app.jinja_env.filters['format_currency'] = format_currency
#     app.jinja_env.globals.update(current_year=current_year)

#     return app.jinja_env

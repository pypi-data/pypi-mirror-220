import logging.config

from flask import Flask
from flask.helpers import get_env

from foo_bar import cmds
from foo_bar.exts import db, migrate, ma, bcrypt, jwt
from foo_bar.router import register_blueprints
from foo_bar.core.errors import TestNewAppShouldBeUndersc0Error, ErrorHandler


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)


def register_shellcontext(app):
    def shell_context():
        return {
            'db': db,
        }
    app.shell_context_processor(shell_context)


def register_commands(app):
    app.cli.add_command(cmds.clean)
    app.cli.add_command(cmds.test)
    app.cli.add_command(cmds.lint)


def register_errorhandlers(app):
    app.register_error_handler(TestNewAppShouldBeUndersc0Error,
                               ErrorHandler.handle_foo_bar)


def register_logging(app):
    logging.config.fileConfig(
        app.config.get('LOG_CONF_PATH'),
        defaults={"logdir": app.config.get('LOG_PATH')})


def create_app(config=None):
    conf_map = {
        'dev': 'development',
        'prod': 'production',
        'test': 'testing'
    }
    config_obj = conf_map.get(config) or get_env()

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(f'foo_bar.config.{config_obj}')
    app.url_map.strict_slashes = False

    register_extensions(app)
    register_shellcontext(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_commands(app)

    if config_obj != 'testing':
        register_logging(app)

    if config_obj == 'production':
        app.config.from_pyfile('prod.secret.cfg', silent=True)
    else:
        from foo_bar.swagger import register_apispec
        register_apispec(app)

    return app

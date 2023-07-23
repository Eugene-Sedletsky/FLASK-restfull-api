"""
    Application Factory Function and configurations for production and testing
"""

import logging
import os
from logging.handlers import RotatingFileHandler
import importlib

import sqlalchemy as sa
from click import echo

from flask import Flask
from flask.logging import default_handler
from flask_sqlalchemy import SQLAlchemy # pylint: disable=import-error


# -------------
# Configuration
# -------------

# Create the instances of the Flask extensions (flask-sqlalchemy etc.) in
# the global scope, but without any arguments passed in.
db = SQLAlchemy()

def create_app():
    """Application Factory Function"""

    app = Flask(__name__)

    config_type = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(config_type)

    initialise_extensions(app)
    configure_logging(app)
    register_cli_commands(app)
    register_blueprints(app)

    engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    inspector = sa.inspect(engine)

    if not inspector.has_table("users"):
        with app.app_context():
            app.logger.info('Cleanup database') # pylint: disable=no-member
            db.drop_all()
            app.logger.info('initialise database') # pylint: disable=no-member
            db.create_all()
    else:
        app.logger.info('Database already contains the users table.')# pylint: disable=no-member

    return app


# ----------------
# Helper Functions
# ----------------
def initialise_extensions(app):
    """Initialise extensions: DB"""
    db.init_app(app)


def configure_logging(app):
    """Configure logging functionality"""
    # Logging Configuration

    file_handler = RotatingFileHandler('instance/management.log',
                                        maxBytes=16384,
                                        backupCount=20)
    # pylint: disable=line-too-long
    file_formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(threadName)s-%(thread)d: %(message)s [in %(filename)s:%(lineno)d]'
    )
    # pylint: enable=line-too-long

    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    # Remove the default logger configured by Flask
    app.logger.removeHandler(default_handler)
    app.logger.info('Starting the Flask User Management App...')


def register_blueprints(app):
    """Register available API blueprints"""

    controllers_path = 'project/http'
    module_base = controllers_path.replace('/', '.')

    for filename in os.listdir(controllers_path):
        if filename.endswith('.py') and filename != '__init__.py':
            app.logger.debug(f'Testing file {filename} in {controllers_path}...')

            module_name = f'{module_base}.{filename[:-3]}'

            app.logger.debug(f'Module name {module_name}...')

            module = importlib.import_module(module_name)

            if hasattr(module, 'controller_blueprint'):
                blueprint = module.controller_blueprint
                app.logger.info(f'Blueprint detected, registering {blueprint} ...')

                app.register_blueprint(module.controller_blueprint)


def register_cli_commands(app):
    """Register CLI commands"""

    @app.cli.command('init_db')
    def initialize_database():
        """Initialize the database."""
        db.drop_all()
        db.create_all()
        echo('Initialized the database!')

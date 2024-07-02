"Handle configuration for an API"
import os

# Determine the folder of the top-level directory of this project
BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', default='BAD_SECRET_KEY')

    # Since SQLAlchemy 1.4.x has removed support for the 'postgres://'
    # URI scheme, update the URI to the postgres database to use
    # the supported 'postgresql://' scheme
    if os.getenv('DATABASE_URL'):
        database_url = os.getenv('DATABASE_URL').replace(
                "postgres://",
                "postgresql://",
                1
            )

        SQLALCHEMY_DATABASE_URI = database_url
    else:
        db_path = os.path.join(BASEDIR, 'instance', 'app.db')
        database_url = f"sqlite:///{db_path}"

        SQLALCHEMY_DATABASE_URI = database_url

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    TESTING = True
    db_path = os.path.join(BASEDIR,'instance','test.db')
    default_url = f"sqlite:///{db_path}"

    database_url = os.getenv( 'TEST_DATABASE_URI', default=default_url)

    SQLALCHEMY_DATABASE_URI = database_url


class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    FLASK_ENV = 'production'

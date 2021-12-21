"""Flask configuration."""
from os import environ, path

from dotenv import load_dotenv

basedir = path.dirname(path.abspath(__file__))
ENV = environ.get('FLASK_ENV', 'default')


if ENV == 'production':
    dotenv_file = '.env.production'
elif ENV == 'development':
    dotenv_file = '.env.development'
else:
    dotenv_file = '.env'

load_dotenv(path.join(basedir, dotenv_file))


class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SWAGGER_UI_OAUTH_CLIENT_ID = environ.get("OAUTH2_CLIENT")
    SWAGGER_UI_OPERATION_ID = True
    SWAGGER_UI_REQUEST_DURATION = True
    SWAGGER_UI_OAUTH_REALM = '-'
    SWAGGER_UI_OAUTH_APP_NAME = 'Flask Rest API'
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{environ.get('DATABASE_USERNAME')}:{environ.get('DATABASE_PASSWORD')}@"
        f"{environ.get('DATABASE_HOST')}:{environ.get('DATABASE_PORT')}/{environ.get('DATABASE_NAME')}"
    )


class ProductionConfig(Config):
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True


class DevelopmentConfig(Config):
    DEBUG = True


class TestConfig(Config):
    DEBUG = True
    TESTING = True
    # For test purpose use a new database
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{environ.get('DATABASE_USERNAME')}:{environ.get('DATABASE_PASSWORD')}@"
        f"{environ.get('DATABASE_HOST')}:{environ.get('DATABASE_PORT')}/{environ.get('TEST_DATABASE_NAME')}"
    )
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class Settings:
    OAUTH2_DOMAIN = environ.get("OAUTH2_DOMAIN")
    OAUTH2_CLIENT = environ.get("OAUTH2_CLIENT")
    OAUTH2_GUEST = environ.get("OAUTH2_GUEST")


settings = Settings()
config_by_name = dict(
    development=DevelopmentConfig,
    production=ProductionConfig,
    default=DevelopmentConfig,
    testing=TestConfig
)

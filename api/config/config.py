"""Flask configuration."""
from os import environ, path

from dotenv import load_dotenv

basedir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
load_dotenv(path.join(basedir, '.env'))


class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SWAGGER_UI_OAUTH_CLIENT_ID = environ.get("OAUTH_CLIENT_ID")
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


class Settings:
    OAUTH_DOMAIN = environ.get("OAUTH_DOMAIN")
    AUTH0_ACCESS_AUDIENCE = environ.get("OAUTH_GUEST_ID")
    AUTH0_ID_AUDIENCE = environ.get("OAUTH_CLIENT_ID")


settings = Settings()

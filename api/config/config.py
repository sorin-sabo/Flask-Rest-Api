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
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{environ.get('DATABASE_USERNAME')}:{environ.get('DATABASE_PASSWORD')}@"
        f"{environ.get('DATABASE_HOST')}:{environ.get('DATABASE_PORT')}/{environ.get('DATABASE_NAME')}"
    )


class ProductionConfig(Config):
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True


class DevelopmentConfig(Config):
    DEBUG = True

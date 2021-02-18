import os


class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.environ.get('username')}:{os.environ.get('password')}@"
        f"{os.environ.get('host')}:{os.environ.get('port')}/{os.environ.get('database')}"
    )


class ProductionConfig(Config):
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True


class DevelopmentConfig(Config):
    DEBUG = True


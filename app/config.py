import os

# import psycopg2 # for working with postgreSQL


class Config(object):
    DEBUG = False
    SECRET_KEY = 'my_secret_key'

    DB_NAME = 'production-db'
    DB_USERNAME = 'root'
    DB_PASSWORD = 'example'

    UPLOADS = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads')

    # For working with uploading file. Not in use for now
    ALLOWED_EXTENSIONS = ["jpg", "png", "mov", "mp4", "mpg"]
    MAX_CONTENT_LENGTH = 1000 * 1024 * 1024


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    DB_NAME = 'blog'
    DB_USERNAME = 'root'
    DB_PASSWORD = 'example'

    SESSION_COOKIE_SECURE = False

    UPLOADS = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads')
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads')
    IMAGE_UPLOADS = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads')
    ALLOWED_EXTENSIONS = ["jpg", "png", "mov", "mp4", "mpg"]
    MAX_CONTENT_LENGTH = 1000 * 1024 * 1024

    # Data Base settings. Now is using SQLlite setting

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'

    # setting PostgreSQL. Does not working. Need in adjustment
    '''
    SQLALCHEMY_DATABASE_URI = os.environ['postgresql://postgresql:example@localhost/database']

    POSTGRES_URL = "127.0.0.1:5433"
    POSTGRES_USER = "postgres"
    POSTGRES_PW = "12345"
    POSTGRES_DB = "test"

    DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL,
                                                                   db=POSTGRES_DB)
    SQLALCHEMY_DATABASE_URI = DB_URL
    '''
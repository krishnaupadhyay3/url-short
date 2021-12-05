import os

basedir = os.path.abspath(os.path.dirname(__file__))


class AppConfig(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(AppConfig):
    DEBUG = False

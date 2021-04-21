import os
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SUBJECT_PREFIX = '[Flaksy]'
    MAIL_SENDER = 'Flasky admin <stylev38@gmail.com>'
    FLASKY_ADMIN = 'stylev38@gmail.com'

    # Mail

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

    POSTS_PER_PAGE = 3

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL', 'postgresql://postgres:1@localhost/test')


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TEST_DATABASE_URL', 'sqlite:///' + os.path.join(BASE_DIR, 'data_test.sqlite3'))


config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig
}

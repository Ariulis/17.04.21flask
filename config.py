import os
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestConfig(Config):
    pass


config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig
}

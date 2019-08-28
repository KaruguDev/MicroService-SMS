import os
import psycopg2
from dotenv import load_dotenv

APP_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(APP_DIR, '..')
TEMPLATE_DIR = os.path.join(APP_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

ENV_PATH = os.path.join(BASE_DIR, '.env')
load_dotenv(ENV_PATH)

class Config:
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASK_ADMIN_SWATCH = 'cerulean'
    STATIC_FOLDER = 'static'

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///{0}/test_micro_sms.db".format(BASE_DIR)
    TESTING = True
    LIVESERVER_PORT = 8900
    LIVESERVER_TIMEOUT = 10

class ProductionConfig(Config):
    DEBUG = False
    #SERVER_NAME = ''


app_config = {
    'development' : Config,
    'production': ProductionConfig,
    'test': TestConfig
}

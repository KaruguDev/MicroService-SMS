import os
import psycopg2

APP_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(APP_DIR, '..')
TEMPLATE_DIR = os.path.join(APP_DIR, 'templates')


class Config:
    SERVER_NAME = 'localhost:5000'
    SECRET_KEY = 
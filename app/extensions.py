from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin


bootsrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
admin = Admin(name='Microservice SMS', template_mode='bootstrap3')

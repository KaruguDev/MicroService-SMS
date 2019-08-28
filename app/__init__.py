from flask import Flask
from .config import Config
from .extensions import db, migrate, admin


app = Flask(__name__, static_folder='static')

#App Configurations
app.config.from_object(Config)


#DB Migrations
db.init_app(app)
from app.models import BulkSMSProvider, DeliveryReport
migrate.init_app(app, db)

#Admin Page
admin.init_app(app)

#import routes
from app import routes

#import admin
from .admin import admin
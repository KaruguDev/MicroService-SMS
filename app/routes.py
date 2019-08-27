from flask import render_template, send_from_directory, url_for, request
from app import app
from .config import STATIC_DIR


@app.route('/')
def index():
    return 'Hello I am running'


@app.route('/static/<path:filename>')
def static(filename):
    return send_from_directory(STATIC_DIR, filename)
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from config import SECRET_KEY
app=Flask(__name__, static_url_path='/app/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'
app.secret_key = SECRET_KEY
from models import db
db.init_app(app)
from app import views

from application import db
from dataclasses import dataclass
from flask_login import UserMixin

@dataclass
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

@dataclass
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    image_id = db.Column(db.Integer)
    model = db.Column(db.String)
    predicted_vegetable = db.Column(db.String)
    predicted_on = db.Column(db.DateTime, nullable=False)

@dataclass
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filepath = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
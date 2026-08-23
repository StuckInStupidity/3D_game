from flask_login import UserMixin
from flask import current_app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(13), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
"""
    items = db.relationship('Item')
    # pour gerer champ RPG

class Item(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
"""
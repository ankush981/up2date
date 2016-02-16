"""Simple wrapper class for DB access"""
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100))
    sites = db.Column(db.String(100))

class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    websites = db.relationship('Website', backref='category')

class Website(db.Model):
    __tablename__ = "websites"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    url = db.Column(db.String(1000), nullable=False)
    class_name = db.Column(db.String(50), nullable=False)
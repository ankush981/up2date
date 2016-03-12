"""Simple wrapper class for DB access"""
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


# class Category(db.Model):
#     __tablename__ = "categories"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, unique=True)
#     websites = db.relationship('websites', backref='category', lazy='dynamic')

# class Website(db.Model):
#     __tablename__ = "websites"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
#     url = db.Column(db.String(1000), nullable=False)
#     class_name = db.Column(db.String(50), nullable=False)
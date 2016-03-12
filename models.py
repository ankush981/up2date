"""Simple wrapper class for DB access"""
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

# relationship table between users and websites
user_website = db.Table('user_website', 
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
                    db.Column('website_id', db.Integer, db.ForeignKey('website.id'), nullable=False),
                    db.PrimaryKeyConstraint('user_id', 'website_id')
                )

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    websites = db.relationship('Website', secondary=user_website, backref='users')
    
    def __repr__(self):
        return '<User %r>' % self.email

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    websites = db.relationship('Website', backref='category', lazy='dynamic')

class Website(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    url = db.Column(db.String(1000), nullable=False)
    class_name = db.Column(db.String(50), nullable=False)
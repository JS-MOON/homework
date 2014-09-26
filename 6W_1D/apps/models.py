"""
models.py

"""

from apps import db
from datetime import datetime, timedelta


def time_now():
    return datetime.utcnow() + timedelta(hours=9)

class User(db.Model):
    email = db.Column(db.String(255), primary_key=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(255))
    join_date = db.Column(db.DateTime(), default=time_now, onupdate=time_now)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text())
    photo = db.Column(db.String(255))
    author = db.Column(db.String(255))
    password = db.Column(db.String(255))
    category1 = db.Column(db.String(255))
    category2 = db.Column(db.String(255))
    like = db.Column(db.Integer)
    date_created = db.Column(db.DateTime(), default=time_now, onupdate=time_now)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    article = db.relationship('Article', backref=db.backref('comments', cascade='all, delete-orphan', lazy='dynamic'))
    author = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    content = db.Column(db.Text())
    like = db.Column(db.Integer)
    date_created = db.Column(db.DateTime(), default=time_now, onupdate=time_now)
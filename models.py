import os
from sqla_wrapper import SQLAlchemy
from datetime import datetime

# this connects to a database either on Heroku or on localhost
db = SQLAlchemy(os.getenv("DATABASE_URL", "sqlite:///localhost.sqlite"))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    secret_number = db.Column(db.Integer)
    passwd = db.Column(db.String)
    session_token = db.Column(db.String)


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    text = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship("User")
    created = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, title, text, author):
        topic = cls(title=title, text=text, author=author)
        db.add(topic)
        db.commit()

        return topic

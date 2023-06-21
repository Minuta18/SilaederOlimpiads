import datetime

from Init import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), index=True, unique=True)
    name = db.Column(db.String(255), index=True)
    last_name = db.Column(db.String(255), index=True)
    middle_name = db.Column(db.String(255), index=True)
    password_hashed = db.Column(db.String(255))
    permissions = db.Column(db.SmallInteger)
    points = db.Column(db.Integer)
    
    is_hidden = db.Column(db.Boolean, default=False)
    is_banned = db.Column(db.SmallInteger, default=False)

    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return '<User %r>' % (self.nickname)
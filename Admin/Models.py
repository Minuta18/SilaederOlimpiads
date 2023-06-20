import datetime
from Init import db

class Olimp(db.Model):
    __tablename__ = 'olimp'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))
    points_for_win = db.Column(db.SmallInteger)
    points_for_prize = db.Column(db.SmallInteger)
    points_for_member = db.Column(db.SmallInteger)

    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now())

    def repr(self):
        return '<Olimp %r>' % (self.id)
import datetime
from Init import db

class Olymp(db.Model):
    __tablename__ = 'olymp'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))
    points_for_win = db.Column(db.SmallInteger)
    points_for_prize = db.Column(db.SmallInteger)
    points_for_member = db.Column(db.SmallInteger)

    is_deleted = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now())

    def repr(self):
        return '<Olymp %r>' % (self.id)

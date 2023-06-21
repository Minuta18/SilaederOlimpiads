import datetime
from Init import db

class Usr_olymp(db.Model):
    __tablename__ = 'usr_olymp'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    olymp_id = db.Column(db.Integer, db.ForeignKey('olymp.id'))
    written_at = db.Column(db.DateTime)
    olymp_klass = db.Column(db.SmallInteger)
    place = db.Column(db.SmallInteger)

    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now())

    def repr(self):
        return '<UsersOlymp %r>' % (self.id)
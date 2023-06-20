import datetime
from Init import db

class Usr_olimp(db.Model):
    __tablename__ = 'usr_olimp'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    olimp_id = db.Column(db.Integer, db.ForeignKey('olimp.id'))
    written_at = db.Column(db.DateTime)
    olimp_klass = db.Column(db.SmallInteger)
    place = db.Column(db.SmallInteger)

    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now())

    def repr(self):
        return '<UsersOlimp %r>' % (self.id)
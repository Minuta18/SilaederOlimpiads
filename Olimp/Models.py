from Init import db

class Usr_olimp(db.Model):
    __tablename__ = 'usr_olimp'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    olimp_id = db.Column(db.Integer, db.ForeignKey('olimp.id'))
    created_at = db.Column(db.DateTime)
    place = db.Column(db.SmallInteger)

    def repr(self):
        return '<UsersOlimp %r>' % (self.id)
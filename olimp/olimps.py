from Init import db
from flask_login import UserMixin

class UsersOlimps(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    olimp_id = db.Column(db.Integer)

    def repr(self):
        return '<UsersOlimp %r>' % (self.id)
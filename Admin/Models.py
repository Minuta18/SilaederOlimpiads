from Init import db

class Olimp(db.Model):
    __tablename__ = 'olimp'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))

    def repr(self):
        return '<Olimp %r>' % (self.id)
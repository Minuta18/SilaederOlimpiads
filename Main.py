from Init import db, app
from Init import Views
from Admin import Views
from Olimp import Views
import Auth

with app.app_context():
    db.create_all()  

if __name__ == "__main__":
    app.run()
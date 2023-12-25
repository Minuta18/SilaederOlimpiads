from Init import db, app
from Init import Views
from Admin import Views
from Olymp import Views
import Auth

with app.app_context():
    db.create_all()  

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=11601)
    
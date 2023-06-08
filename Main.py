from Init import db, app
import Auth

with app.app_context():
    db.create_all()  

if __name__ == "__main__":
    app.run()
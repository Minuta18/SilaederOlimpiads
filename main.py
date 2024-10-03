from init import db, app
from init import views
from admin import views
from olymp import views
import auth

with app.app_context():
    db.create_all()  

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=11601)
    
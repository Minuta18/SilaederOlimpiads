from Init import login_manager
from Init import app
from Init import db
from .Models import User

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

from . import Views
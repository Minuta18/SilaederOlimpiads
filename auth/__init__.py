from init import login_manager
from init import app
from init import db
from .models import User

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

from . import views
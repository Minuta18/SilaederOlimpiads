from flask_login import current_user
from enum import Enum 

class Permissions(Enum):
    default = 0
    admin = 1

def is_admin():
    if current_user.is_authenticated:
        if current_user.permissions == Permissions.admin.value:
            return True
    return False
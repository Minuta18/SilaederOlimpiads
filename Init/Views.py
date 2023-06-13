from flask_login import current_user
from . import app

@app.route('/')
def index():
    if not current_user.is_authenticated:
        return '''You are not authenticated, loh'''
    return f'''Hello, {current_user.name}''' 
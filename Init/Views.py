from flask import Flask, render_template, request, redirect, abort
from flask_login import login_user, login_required, logout_user, current_user
from Auth import User
from . import app

@app.route('/')
def index():
    if not current_user.is_authenticated:
        return '''You are not authenticated, loh'''
    return f'''Hello, {current_user.name}''' 

@app.route('/user/<user_id>')
def user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404)

    username = f'{user.name} {user.last_name} {user.middle_name}' 

    return render_template(
        'init/User.html', 
        username=username,
        user=user,
    )
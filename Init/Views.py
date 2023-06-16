from flask import Flask, render_template, request, redirect, abort
from flask_login import login_user, login_required, logout_user, current_user
from Auth import User
from . import app

@app.route('/')
def index():
    return render_template('init/Index.html', usr=current_user)

@app.route('/user/<user_id>')
def user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404)

    username = f'{user.name} {user.last_name} {user.middle_name}' 

    return render_template(
        'init/User.html', 
        username=username,
        usr=current_user,
        user=user,
    )
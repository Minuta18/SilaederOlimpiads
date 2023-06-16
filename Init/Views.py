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

@app.route('/leaderboard/')
def leaderboard():
    users = list()
    for ind, user in enumerate(User.query.order_by(User.points.desc()).limit(15).all()):
        users.append({
            'place': ind + 1,
            'name': f'{user.name} {user.last_name} {user.middle_name}',
            'points': user.points,
        })

    return render_template(
        'init/Leaderboard.html',
        usr=current_user,
        users=users,
    )

@app.errorhandler(400)
def error400(err):
    return render_template('init/Error.html', usr=current_user, error_code=400), 400

@app.errorhandler(401)
def error401(err):
    return render_template('init/Error.html', usr=current_user, error_code=401), 401

@app.errorhandler(403)
def error403(err):
    return render_template('init/Error.html', usr=current_user, error_code=403), 403

@app.errorhandler(404)
def error404(err):
    return render_template('init/Error.html', usr=current_user, error_code=404), 404

@app.errorhandler(405)
def error405(err):
    return render_template('init/Error.html', usr=current_user, error_code=405), 405

@app.errorhandler(500)
def error500(err):
    return render_template('init/Error.html', usr=current_user, error_code=500), 500
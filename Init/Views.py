from flask import Flask, render_template, request, redirect, abort
from flask_login import login_user, login_required, logout_user, current_user
from Auth import User
from Auth.Permissions import is_admin
from . import app

@app.route('/')
def index():
    return render_template('init/Index.html', usr=current_user, is_admin=is_admin())

@app.route('/user/<user_id>')
def user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404)

    if user.is_hidden:
        if not (is_admin() or user.id == current_user.id):
            abort(403)

    username = f'{user.name} {user.last_name} {user.middle_name}' 

    return render_template(
        'init/User.html', 
        username=username,
        usr=current_user,
        user=user,
        is_admin=is_admin(),
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
        is_admin=is_admin(),
    )

@app.errorhandler(400)
def error400(err):
    return render_template('init/Error.html', usr=current_user, error_code=400, is_admin=is_admin()), 400

@app.errorhandler(401)
def error401(err):
    return render_template('init/Error.html', usr=current_user, error_code=401, is_admin=is_admin()), 401

@app.errorhandler(403)
def error403(err):
    return render_template('init/Error.html', usr=current_user, error_code=403, is_admin=is_admin()), 403

@app.errorhandler(404)
def error404(err):
    return render_template('init/Error.html', usr=current_user, error_code=404, is_admin=is_admin()), 404

@app.errorhandler(405)
def error405(err):
    return render_template('init/Error.html', usr=current_user, error_code=405, is_admin=is_admin()), 405

@app.errorhandler(500)
def error500(err):
    return render_template('init/Error.html', usr=current_user, error_code=500, is_admin=is_admin()), 500
from functools import wraps
from flask import Flask, render_template, request, redirect, abort
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError, PendingRollbackError
from Init import app, db
from .Models import Olimp
from Olimp.Models import Usr_olimp
from Auth.Permissions import Permissions

def admin_only(name):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(403)
            if current_user.permissions != Permissions.admin.value():
                abort(403)
            return func(*args, **kwargs)
        return wrapped
    return decorator

@app.route('/admin/add/', methods=['GET', 'POST'])
@admin_only('add_olimp')
def add_olimp():
    if request.method == 'POST':
        name = request.form.get('name')
        desc = request.form.get('desc')

        try:
            new_olimp = Olimp(name=name, description=desc)

            db.session.add(new_olimp)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return render_template('admin/Add.html', code=1)

        return redirect('/admin/')
    return render_template('admin/Add.html', code=0) # TODO

@app.route('/admin/', methods=['GET', 'POST'])
@admin_only('all_olimps')
def all_olimps():
    return render_template('admin/Index.html', olimps=Olimp.query.filter(id==id))

@app.route('/admin/list', methods=['GET', 'POST'])
@admin_only('list_olimps')
def list_olimps():
    return render_template('admin/List.html', olimps=Usr_olimp.query.filter(id==id))
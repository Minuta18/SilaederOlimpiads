from flask import Flask, render_template, request, redirect, abort
from flask_login import login_user, login_required, logout_user, current_user
from Init import app, db
from .Models import Olimp
from Olimp.Models import Usr_olimp
from Auth.Permissions import Permissions

def admin_only(func):
    def wrapper():
        if not current_user.is_authenticated:
            abort(403)
        if current_user.permissions != Permissions.admin.value():
            abort(403)
        func()
    return wrapper

@admin_only
@app.route('/admin/add/', methods=['GET', 'POST'])
def add_olimp():
    if request.method == 'POST':
        name = request.form.get('name')
        desc = request.form.get('desc')

        # try:
        new_olimp = Olimp(name=name, description=desc)

        db.session.add(new_olimp)
        db.session.commit()
        # except:
        #     return render_template('admin/Add.html', code=1)

        return redirect('/admin/')
    return render_template('admin/Add.html', code=0) # TODO

@admin_only
@app.route('/admin/', methods=['GET', 'POST'])
def all_olimps():
    return render_template('admin/Index.html', olimps=Olimp.query.filter(id==id))

@admin_only
@app.route('/admin/list', methods=['GET', 'POST'])
def list_olimps():
    return render_template('admin/List.html', olimps=Usr_olimp.query.filter(id==id))
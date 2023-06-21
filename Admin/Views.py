from functools import wraps
from flask import Flask, render_template, request, redirect, abort
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError, PendingRollbackError
from Init import app, db
from .Models import Olymp
from Olymp.Models import Usr_olymp
from Olymp.Place import Place
from Auth.Permissions import Permissions
from Auth import User

def admin_only(name):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(403)
            if current_user.permissions != Permissions.admin.value:
                abort(403)
            return func(*args, **kwargs)
        return wrapped
    return decorator

@app.route('/admin/', methods=['GET', 'POST'])
@admin_only('admin_panel')
def admin_panel():
    return render_template('admin/Admin.html', usr=current_user)

@app.route('/admin/add/', methods=['GET', 'POST'])
@admin_only('add_olymp')
def add_olymp():
    if request.method == 'POST':
        name = request.form.get('name')
        desc = request.form.get('desc')
        pfw = request.form.get('pfw')
        pfp = request.form.get('pfp')
        pfm = request.form.get('pfm')

        try:
            new_olymp = Olymp(
                name=name, 
                description=desc,
                points_for_win=pfw,
                points_for_prize=pfp,
                points_for_member=pfm,
            )

            db.session.add(new_olymp)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return render_template('admin/Add.html', code=1, usr=current_user)

        return redirect('/admin/')
    return render_template('admin/Add.html', code=0, usr=current_user) # TODO

@app.route('/admin/olymp_list/', methods=['GET', 'POST'])
@admin_only('list_olymps')
def list_olymps(): # TODO: rewrite in C
    olymps = Usr_olymp.query.all()
    dicted_olymps = list()
    for olymp in olymps:
        Usr = User.query.get(olymp.user_id)
        place = ''
        if olymp.place == Place.winner.value:
            place = 'Победитель'
        elif olymp.place == Place.prizewinner.value:
            place = 'Призёр'
        else:
            place = 'Участник'
        dicted_olymps.append({
            'id': int(olymp.olymp_id),
            'name': str(Olymp.query.get(olymp.olymp_id).name),
            'klass': int(olymp.olymp_klass),
            'user': str(f'{Usr.name} {Usr.last_name} {Usr.middle_name}'),
            'user_id': int(f'{Usr.id}'),
            'place': str(place),
        })

    if request.method == 'POST':
        if request.form.get('usr_name') != '':
            name = request.form.get('usr_name').lower()
            dicted_olymps = [olymp for olymp in dicted_olymps if name.lower() in olymp['user'].lower()]
        if request.form.get('oli_name') != '':
            oli = request.form.get('oli_name').lower()
            dicted_olymps = [olymp for olymp in dicted_olymps if oli.lower() in olymp['name'].lower()]
        if request.form.get('oli_klass') != '':
            kls = request.form.get('oli_klass').lower()
            dicted_olymps = [olymp for olymp in dicted_olymps if int(kls) == olymp['klass']]
        if request.form.get('filtering') != 0:
            val = int(request.form.get('filtering'))
            if val == 1:
                dicted_olymps = [olymp for olymp in dicted_olymps if olymp['place'] == 'Победитель']
            elif val == 2:
                dicted_olymps = [olymp for olymp in dicted_olymps if olymp['place'] == 'Призёр']
            elif val == 3:
                dicted_olymps = [olymp for olymp in dicted_olymps if olymp['place'] == 'Участник']
        if request.form.get('sorting1') != '0':
            if request.form.get('sorting1') == '1':
                dicted_olymps.sort(key=lambda olymp: olymp['user'])
            else:
                dicted_olymps.sort(key=lambda olymp: olymp['user'], reverse=True)
        elif request.form.get('sorting2') != '0':
            if request.form.get('sorting2') == '1':
                dicted_olymps.sort(key=lambda olymp: olymp['place'])
            else:
                dicted_olymps.sort(key=lambda olymp: olymp['place'], reverse=True)
        elif request.form.get('sorting3') != '0':
            if request.form.get('sorting3') == '1':
                dicted_olymps.sort(key=lambda olymp: olymp['klass'])
            else:
                dicted_olymps.sort(key=lambda olymp: olymp['klass'], reverse=True)
    return render_template(
        'admin/List.html', 
        usr=current_user,
        olymps=dicted_olymps,
    )
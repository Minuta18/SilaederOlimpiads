from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, abort, url_for
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError, PendingRollbackError
from Init import app, db
from .Models import Olymp
from Olymp.Models import Usr_olymp
from Olymp.Place import Place
from Auth.Permissions import Permissions, is_admin, is_banned
from Auth import User

def admin_only(name):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(403)
            if not is_admin():
                abort(403)
            return func(*args, **kwargs)
        return wrapped
    return decorator

def not_banned(name):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if current_user.is_authenticated():
                if is_banned():
                    return redirect(url_for('got_banned'))
            return func(*args, **kwargs)
        return wrapped
    return decorator

@app.route('/admin/', methods=['GET', 'POST'])
@admin_only('admin_panel')
@not_banned('admin_panel')
def admin_panel():
    return render_template('admin/Admin.html', usr=current_user)

@app.route('/admin/usr_olymp_list/', methods=['GET', 'POST'])
@admin_only('list_usr_olymps')
@not_banned('list_usr_olymps')
def list_usr_olymps(): # TODO: rewrite in C
    olymps = Usr_olymp.query.join(Olymp).filter(~(Olymp.is_deleted))
    dicted_olymps = list()
    for olymp in olymps:
        Usr = User.query.get(olymp.user_id)
        Olp = Olymp.query.get(olymp.olymp_id)
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

@app.route('/admin/olymp_list/', methods=['GET', 'POST'])
@admin_only('list_olymps')
@not_banned('list_olymps')
def list_olymps():
    olymps = [{
        'id': int(olymp.id),
        'name': str(olymp.name),
        'date': olymp.created_at.strftime('%Y.%m.%d'),
        'is_deleted': bool(olymp.is_deleted),
    } for olymp in Olymp.query.all()]
    return render_template(
        'olymp/List.html',
        olymps=olymps,
        usr=current_user,
    )

@app.route('/admin/usr_list/', methods=['GET', 'POST'])
@admin_only('usr_list')
@not_banned('usr_list')
def usr_list():
    users = [{
        'id': usr.id,
        'email': usr.email,
        'name': f'{usr.name} {usr.last_name} {usr.middle_name}',
        'date': usr.updated_at,
        'status': (f'Забанен' if usr.is_banned else 'Всё нормально'),
        'banned': usr.is_banned,
        'points': usr.points,
    } for usr in User.query.all()]
    return render_template(
        'auth/List.html',
        users=users,
        usr=current_user,
    )
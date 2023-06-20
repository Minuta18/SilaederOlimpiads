from functools import wraps
from flask import Flask, render_template, request, redirect, abort
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError, PendingRollbackError
from Init import app, db
from .Models import Olimp
from Olimp.Models import Usr_olimp
from Olimp.Place import Place
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
@admin_only('add_olimp')
def add_olimp():
    if request.method == 'POST':
        name = request.form.get('name')
        desc = request.form.get('desc')
        pfw = request.form.get('pfw')
        pfp = request.form.get('pfp')
        pfm = request.form.get('pfm')

        try:
            new_olimp = Olimp(
                name=name, 
                description=desc,
                points_for_win=pfw,
                points_for_prize=pfp,
                points_for_member=pfm,
            )

            db.session.add(new_olimp)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return render_template('admin/Add.html', code=1, usr=current_user)

        return redirect('/admin/')
    return render_template('admin/Add.html', code=0, usr=current_user) # TODO

@app.route('/admin/olimp_list/', methods=['GET', 'POST'])
@admin_only('list_olimps')
def list_olimps(): # TODO: rewrite in C
    olimps = Usr_olimp.query.all()
    dicted_olimps = list()
    for olimp in olimps:
        Usr = User.query.get(olimp.user_id)
        place = ''
        if olimp.place == Place.winner.value:
            place = 'Победитель'
        elif olimp.place == Place.prizewinner.value:
            place = 'Призёр'
        else:
            place = 'Участник'
        dicted_olimps.append({
            'id': int(olimp.olimp_id),
            'name': str(Olimp.query.get(olimp.olimp_id).name),
            'klass': int(olimp.olimp_klass),
            'user': str(f'{Usr.name} {Usr.last_name} {Usr.middle_name}'),
            'user_id': int(f'{Usr.id}'),
            'place': str(place),
        })

    if request.method == 'POST':
        if request.form.get('usr_name') != '':
            name = request.form.get('usr_name').lower()
            dicted_olimps = [olimp for olimp in dicted_olimps if name.lower() in olimp['user'].lower()]
        if request.form.get('oli_name') != '':
            oli = request.form.get('oli_name').lower()
            dicted_olimps = [olimp for olimp in dicted_olimps if oli.lower() in olimp['name'].lower()]
        if request.form.get('oli_klass') != '':
            kls = request.form.get('oli_klass').lower()
            dicted_olimps = [olimp for olimp in dicted_olimps if int(kls) == olimp['klass']]
        if request.form.get('filtering') != 0:
            val = int(request.form.get('filtering'))
            if val == 1:
                dicted_olimps = [olimp for olimp in dicted_olimps if olimp['place'] == 'Победитель']
            elif val == 2:
                dicted_olimps = [olimp for olimp in dicted_olimps if olimp['place'] == 'Призёр']
            elif val == 3:
                dicted_olimps = [olimp for olimp in dicted_olimps if olimp['place'] == 'Участник']
        if request.form.get('sorting1') != '0':
            if request.form.get('sorting1') == '1':
                dicted_olimps.sort(key=lambda olimp: olimp['user'])
            else:
                dicted_olimps.sort(key=lambda olimp: olimp['user'], reverse=True)
        elif request.form.get('sorting2') != '0':
            if request.form.get('sorting2') == '1':
                dicted_olimps.sort(key=lambda olimp: olimp['place'])
            else:
                dicted_olimps.sort(key=lambda olimp: olimp['place'], reverse=True)
        elif request.form.get('sorting3') != '0':
            if request.form.get('sorting3') == '1':
                dicted_olimps.sort(key=lambda olimp: olimp['klass'])
            else:
                dicted_olimps.sort(key=lambda olimp: olimp['klass'], reverse=True)
    return render_template(
        'admin/List.html', 
        usr=current_user,
        olimps=dicted_olimps,
    )
import datetime
import re
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, abort, url_for
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message
from sqlalchemy.exc import IntegrityError
from Init import db
from .Models import User
from Admin.Models import Olymp
from Olymp.Models import get_place, Usr_olymp
from Init import app
from Admin.Views import admin_only, not_banned
from .Permissions import Permissions, is_admin, is_banned

def not_login_required(name):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if current_user.is_authenticated:
                return redirect('/')
            return func(*args, **kwargs)
        return wrapped
    return decorator

def check_email(email: str) -> bool:
    return not re.fullmatch(
        re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), 
        email,  
    ) == None

@app.route('/user/<user_id>')
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404)

    if user.is_hidden:
        if not (is_admin() or user.id == current_user.id):
            abort(403)

    username = f'{user.name} {user.last_name} {user.middle_name}' 
    written_olymps = [{
        'id': int(olymp.id),
        'name': f'{str(Olymp.query.get(olymp.olymp_id).name)}, {int(olymp.olymp_klass)} класс',
        'place': get_place(olymp.place),
    } for olymp in Usr_olymp.query.all()]

    return render_template(
        'init/User.html', 
        username=username,
        usr=current_user,
        user=user,
        written_olymps=written_olymps,
        len_written_olymps=len(written_olymps),
        is_admin=is_admin(),
    )

@app.route('/user/login/', methods=['GET', 'POST'])
@not_login_required('login')
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user == None:
            return render_template('auth/Login.html', code=1, email=email, password=password)
        
        if not check_password_hash(user.password_hashed, password):
            return render_template('auth/Login.html', code=2, email=email, password=password)

        login_user(user)
        return redirect(url_for('index'))
    return render_template('auth/Login.html', code=0, email='', password='')

@app.route('/user/register/', methods=['GET', 'POST'])
@not_login_required('register')
def register():
    #! THIS IS A DEPRECATED METHOD 
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        surname = request.form.get('surname')
        midname = request.form.get('midname')
        password = request.form.get('pass')
        password_confirmation = request.form.get('pass2')

        new_user = User(
            email=email,
            name=name,
            last_name=surname,
            middle_name=midname,
            password_hashed=generate_password_hash(password, method='scrypt'),
            permissions=Permissions.default.value,
            points=0,
        )

        if not check_email(email):
            return render_template('auth/Register.html', code=5, new_user=new_user) 

        if not request.form.get('accept'):
            return render_template('auth/Register.html', code=3, new_user=new_user) 

        if password != password_confirmation:
            return render_template('auth/Register.html', code=1, new_user=new_user)
        
        if False: # TODO: add validation if user is not in silaeder
            return render_template('auth/Register.html', code=2, new_user=new_user)

        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return render_template('auth/Register.html', code=4, new_user=new_user)
        login_user(new_user)

        return redirect(url_for('index'))
    return render_template('auth/Register.html', code=0, new_user=User(
        email='', name='', last_name='', middle_name='', 
        password_hashed='', permissions=Permissions.default.value,
    ))

@app.route('/user/logout/', methods=['GET'])
@login_required
def logout():
    logout_user()

    return redirect(url_for('index'))

@app.route('/user/edit/', methods=['GET', 'POST'])
@login_required
def edit():
    cuser = User.query.get(current_user.id)
    default_tab = request.args.get('tab')
    if request.args.get('action') == 'hide':
        cuser.is_hidden = not cuser.is_hidden
        db.session.commit()

    if request.method == 'POST':
        form = int(request.args.get('form'))
        if form == 1:
            try:
                cuser.email = request.form.get('email')    
                if not check_email(cuser.email):
                    return render_template('auth/Register.html', code=4, new_user=cuser) 

                cuser.name = request.form.get('name')
                cuser.last_name = request.form.get('surname')
                cuser.middle_name = request.form.get('midname')
            except IntegrityError:
                return render_template('auth/Edit.html', usr=cuser, code=1, defaultOpen=1, is_admin=is_admin())
        elif form == 2:
            old_pass = request.form.get('old-pass')
            new_pass = request.form.get('new-pass')
            new_pass_repeat = request.form.get('new-pass-repeat')

            if check_password_hash(cuser.password_hashed, old_pass):
                if new_pass != new_pass_repeat:
                    return render_template('auth/Edit.html', usr=cuser, code=2, defaultOpen=2, is_admin=is_admin())
                cuser.password_hashed = generate_password_hash(new_pass, method='scrypt')
            else:
                return render_template('auth/Edit.html', usr=cuser, code=3, defaultOpen=2, is_admin=is_admin())
            
        cuser.updated_at = datetime.datetime.now()
        db.session.commit()

    return render_template(
        'auth/Edit.html', 
        usr=cuser, 
        code=0, 
        defaultOpen=int(default_tab) if default_tab != None else 1, 
        is_admin=is_admin()
    )

@app.route('/user/<user_id>/ban/', methods=['POST', 'GET'])
@admin_only('ban_user')
@not_banned('ban_user')
def ban_user(user_id):
    usr = User.query.get(user_id)

    if usr.permissions == Permissions.dev.value and \
        current_user.permissions == Permissions.admin.value:
        abort(403)

    if usr.is_banned:
        usr.is_banned = False
        db.session.add(usr)
        db.session.commit()

        return redirect(url_for('usr_list'))
    
    if request.method == 'POST':
        usr.is_banned = True
        db.session.add(usr)
        db.session.commit()
        
        return redirect(url_for('usr_list'))

    return render_template('auth/Ban.html', usr=current_user, )

@app.route('/banned/', methods=['POST', 'GET'])
def got_banned():
    return render_template('auth/GotBanned.html', usr=current_user, )


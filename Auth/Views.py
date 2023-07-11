import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, abort, url_for
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError
from Init import db
from .Models import User
from Admin.Models import Olymp
from Olymp.Models import get_place, Usr_olymp
from Init import app
from .Permissions import Permissions, is_admin

def not_login_required(name):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if current_user.is_authenticated:
                return redirect('/')
            return func(*args, **kwargs)
        return wrapped
    return decorator

@app.route('/user/<user_id>')
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404)

    if user.is_hidden:
        if not (is_admin() or user.id == current_user.id):
            abort(403)

    username = f'{user.name} {user.last_name} {user.middle_name}' 
    writed_olymps = [{
        'id': int(olymp.id),
        'name': f'{str(Olymp.query.get(olymp.olymp_id).name)}, {int(olymp.olymp_klass)} класс',
        'place': get_place(olymp.place),
    } for olymp in Usr_olymp.query.all()]

    return render_template(
        'init/User.html', 
        username=username,
        usr=current_user,
        user=user,
        writed_olymps=writed_olymps,
        len_writed_olymps=len(writed_olymps),
        is_admin=is_admin(),
    )

@app.route('/user/login/', methods=['GET', 'POST'])
@not_login_required('login')
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        passw = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user == None:
            return render_template('auth/Login.html', code=1, email=email, password=passw)
        
        if not check_password_hash(user.password_hashed, passw):
            return render_template('auth/Login.html', code=2, email=email, password=passw)

        login_user(user)
        return redirect(url_for('index'))
    return render_template('auth/Login.html', code=0, email='', password='')

@app.route('/user/register/', methods=['GET', 'POST'])
@not_login_required('registred')
def register():
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
            permissions=Permissions.dev.value,
            points=0,
        )

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

    return redirect(url_for('/'))

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
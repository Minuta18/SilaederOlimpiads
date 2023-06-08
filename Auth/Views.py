from Init import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect
from flask_login import login_user, login_required, logout_user
from .Models import User
from Init import app

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        passw = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user:
            return render_template('Login.html', code=1)
        
        if not check_password_hash(user.password_hashed, passw):
            return render_template('Login.html', code=2)

        login_user(user)
        return redirect('/')
    return render_template('Login.html', code=0)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        surname = request.form.get('surname')
        midname = request.form.get('midname')
        klass = request.form.get('klass')
        password = request.form.get('password')
        password_confirmation = request.form.get('password_confirmation')

        if password != password_confirmation:
            return render_template('Register.html', code=1)
        
        if False: # TODO: add validation if user is not in silaeder
            return render_template('Register.html', code=2)

        new_user = User(
            email=email,
            name=name,
            last_name=surname,
            middle_name=midname,
            klass=klass,
            password_hashed=generate_password_hash(password, method='sha256')
        )

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)

        return redirect('/')
    return render_template('Register.html', code=0)

@login_required
@app.route('/logout/', methods=['GET'])
def logout():
    logout_user()

    return redirect('/')
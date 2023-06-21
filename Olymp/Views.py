from datetime import date, datetime
from .Models import Usr_olymp
from Admin.Models import Olymp
from Auth.Models import User 
from Auth.Permissions import is_admin
from .Place import Place
from Init import app, db
from flask_login import login_required, current_user
from flask import Flask, render_template, request, redirect, abort

@app.route('/add/', methods=['GET', 'POST'])
@login_required
def add_olymp_for_user():
    if request.method == 'POST':
        olymp = request.form.get('olymp')
        date_ = request.form.get('date')
        klass_ = request.form.get('klass')
        place = int(request.form.get('place'))

        olymp = Olymp.query.filter_by(name=olymp).first()
        if not olymp:
            return render_template('olymp/Add.html', code=1, usr=current_user, is_admin=is_admin())
        
        used_olymp = Usr_olymp.query.filter_by(
            user_id=current_user.id, 
            olymp_id=olymp.id, 
            olymp_klass=klass_,
            written_at=datetime.strptime(date_, '%Y-%m-%d')
        ).first()
        if used_olymp != None:
            return render_template('olymp/Add.html', code=2, usr=current_user, is_admin=is_admin())
        
        new_olymp = Usr_olymp(
            user_id=current_user.id,
            olymp_id=olymp.id,
            olymp_klass=klass_,
            written_at=datetime.strptime(date_, '%Y-%m-%d'),
            place=place,
        )

        if place == 0:
            current_user.points += olymp.points_for_win
        elif place == 1:
            current_user.points += olymp.points_for_prize
        elif place == 2:
            current_user.points += olymp.points_for_member

        db.session.add(new_olymp)
        db.session.commit()

        return redirect('/')
    return render_template('olymp/Add.html', code=0, usr=current_user, olymps=Olymp.query.all(), is_admin=is_admin())

@app.route('/olymp/<olymp_id>/')
def get_olymp(olymp_id):
    olymp = Olymp.query.get(olymp_id)
    if olymp == None:
        abort(404)

    return render_template('olymp/Olymp.html', olymp=olymp, usr=current_user, is_admin=is_admin())
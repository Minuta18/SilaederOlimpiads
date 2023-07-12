from datetime import date, datetime
from .Models import Usr_olymp
from Admin.Models import Olymp
from Admin.Views import admin_only, not_banned
from Auth.Models import User 
from Auth.Permissions import is_admin
from .Place import Place
from Init import app, db
from flask_login import login_required, current_user
from flask import Flask, render_template, request, redirect, abort, url_for
from sqlalchemy.exc import IntegrityError, PendingRollbackError

@app.route('/olymp/add/', methods=['GET', 'POST'])
@login_required
@not_banned('add_olymp')
def add_olymp():
    if request.method == 'POST':
        olymp = request.form.get('olymp')
        date_ = request.form.get('date')
        klass_ = request.form.get('klass')
        place = int(request.form.get('place'))

        olymp = Olymp.query.filter((Olymp.name == olymp) & (~Olymp.is_deleted)).first()
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

        return redirect(url_for('index'))
    return render_template('olymp/Add.html', code=0, usr=current_user, olymps=Olymp.query.filter(~Olymp.is_deleted), is_admin=is_admin())

@app.route('/olymp/<olymp_id>/')
def olymp(olymp_id):
    olymp = Olymp.query.get(olymp_id)
    if olymp == None:
        abort(404)

    return render_template('olymp/Olymp.html', olymp=olymp, usr=current_user, is_admin=is_admin())

@app.route('/olymp/register', methods=['GET', 'POST'])
@admin_only('reqister_olymp')
@not_banned('register_olymp')
def register_olymp():
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
            return render_template('admin/Add.html', code=1, usr=current_user, olymp=new_olymp)

        return redirect(url_for('admin_panel'))
    return render_template('admin/Add.html', code=0, usr=current_user, olymp=Olymp(
        name='',
        description='',
        points_for_win=0,
        points_for_prize=0,
        points_for_member=0,
    ))

@app.route('/olymp/<olymp_id>/edit/', methods=['GET', 'POST'])
@admin_only('edit_olymp')
@not_banned('edit_olymp')
def edit_olymp(olymp_id):
    olymp = Olymp.query.get(olymp_id)

    if request.method == 'POST':
        olymp.name =  request.form.get('name')
        olymp.description = request.form.get('desc')
        olymp.points_for_win = request.form.get('pfw')
        olymp.points_for_prize = request.form.get('pfp')
        olymp.points_for_member = request.form.get('pfm')
        olymp.update_at = datetime.now()
            
        try:
            db.session.add(olymp)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return render_template('admin/Add.html', code=1, usr=current_user, olymp=olymp)
        return redirect(url_for('admin_panel'))
    return render_template(
        'admin/Add.html',
        code=0,
        usr=current_user,
        olymp=olymp,
    )

@app.route('/olymp/<olymp_id>/delete/', methods=['GET'])
@admin_only('delete_olymp')
@not_banned('delete_olymp')
def delete_olymp(olymp_id):
    olymp = Olymp.query.get(olymp_id)
    olymp.is_deleted = not olymp.is_deleted

    for usr_olymp in Usr_olymp.query.join(Olymp).filter(Olymp.name == olymp.name):
        usr = User.query.get(usr_olymp.user_id)
        if olymp.is_deleted:
            if usr_olymp.place == 0:
                usr.points -= olymp.points_for_win
            elif usr_olymp.place == 1:
                usr.points -= olymp.points_for_prize
            elif usr_olymp.place == 2:
                usr.points -= olymp.points_for_member
        else:
            if usr_olymp.place == 0:
                usr.points += olymp.points_for_win
            elif usr_olymp.place == 1:
                usr.points += olymp.points_for_prize
            elif usr_olymp.place == 2:
                usr.points += olymp.points_for_member
        db.session.add(usr)
        
    db.session.add(olymp)
    db.session.commit()

    return redirect(url_for('admin_panel'))
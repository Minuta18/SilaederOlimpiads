from datetime import date, datetime
from .Models import Usr_olimp
from Admin.Models import Olimp
from Auth.Models import User 
from Auth.Permissions import is_admin
from .Place import Place
from Init import app, db
from flask_login import login_required, current_user
from flask import Flask, render_template, request, redirect, abort

@app.route('/add/', methods=['GET', 'POST'])
@login_required
def add_olimp_for_user():
    if request.method == 'POST':
        olimp = request.form.get('olimp')
        date_ = request.form.get('date')
        place = int(request.form.get('place'))

        olimp = Olimp.query.filter_by(name=olimp).first()
        if not olimp:
            return render_template('olimp/Add.html', code=1, usr=current_user, is_admin=is_admin())
        
        used_olimp = Usr_olimp.query.filter_by(
            user_id=current_user.id, 
            olimp_id=olimp.id, 
            created_at=datetime.strptime(date_, '%Y-%m-%d')
        ).first()
        if used_olimp != None:
            return render_template('olimp/Add.html', code=2, usr=current_user, is_admin=is_admin())
        
        new_olimp = Usr_olimp(
            user_id=current_user.id,
            olimp_id=olimp.id,
            created_at=datetime.strptime(date_, '%Y-%m-%d'),
            place=place,
        )

        if place == 0:
            current_user.points += olimp.points_for_win
        elif place == 1:
            current_user.points += olimp.points_for_prize
        elif place == 2:
            current_user.points += olimp.points_for_member

        db.session.add(new_olimp)
        db.session.commit()

        return redirect('/')
    return render_template('olimp/Add.html', code=0, usr=current_user, olimps=Olimp.query.all(), is_admin=is_admin())

@app.route('/olimp/<olimp_id>/')
def get_olimp(olimp_id):
    olimp = Olimp.query.get(olimp_id)
    if olimp == None:
        abort(404)

    return render_template('olimp/Olimp.html', olimp=olimp, usr=current_user, is_admin=is_admin())
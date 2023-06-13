from datetime import date, datetime
from .Models import Usr_olimp
from Admin.Models import Olimp
from Auth.Models import User 
from Init import app, db
from flask_login import login_required, current_user
from flask import Flask, render_template, request, redirect

@login_required
@app.route('/add/', methods=['GET', 'POST'])
def add_olimp_for_user():
    if request.method == 'POST':
        olimp = request.form.get('olimp')
        date_ = request.form.get('date')
        place = request.form.get('place')

        olimp = Olimp.query.filter_by(name=olimp).first()
        if not olimp:
            return render_template('olimp/Add.html', code=1)
        
        used_olimp = Usr_olimp.query.filter_by(user_id=current_user.id, olimp_id=olimp.id, created_at=datetime.strptime(date_, '%m-%d-%Y')).first()
        if used_olimp != None:
            return render_template('olimp/Add.html', code=2)
        
        new_olimp = Usr_olimp(
            user_id=current_user.id,
            olimp_id=olimp.id,
            created_at=datetime.strptime(date_, '%m-%d-%Y'),
            place=place,
        )
        db.session.add(new_olimp)
        db.session.commit()

        return redirect('/')
    return render_template('olimp/Add.html')
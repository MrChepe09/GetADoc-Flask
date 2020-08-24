from secrets import token_hex
from flask import render_template, url_for, redirect, flash, request
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, DoctorRegister, PatientRegister
from app.models import Patient, Doctor
from werkzeug.urls import url_parse

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
@login_required
def about():
	return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        if(form.choice.data == 'Patient'):
            daba = Patient
        else:
            daba = Doctor
        user = daba.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', form=form)

@app.route('/register/<choice>', methods=['GET', 'POST'])
def register(choice):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    idd = token_hex(16)
    if(choice=='doctor'):
        idd = 'D'+idd
        form = DoctorRegister()
        if form.validate_on_submit():
            user = Doctor(id = idd, full_name=form.name.data, email=form.email.data, city=form.city.data, phone=form.phone.data, address=form.address.data, qual=form.qual.data, fees=form.fees.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
    else:
        idd = 'P'+idd
        form = PatientRegister()
        if form.validate_on_submit():
            user = Patient(id=idd, full_name=form.name.data, email=form.email.data, city=form.city.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
    
    return render_template('register.html', choice=choice, form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
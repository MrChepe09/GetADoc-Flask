from secrets import token_hex
from flask import render_template, url_for, redirect, flash, request
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, DoctorRegister, PatientRegister, AppointmentForm, confirmAppointment, rejectAppointment
from app.models import Patient, Doctor, Appointment
from werkzeug.urls import url_parse
from datetime import datetime

@app.route('/')
def home():
    date = datetime.utcnow()
    return render_template('home.html', date=date)

@app.route('/about')
@login_required
def about():
	return render_template('about.html')

@app.route('/finddoctor')
@login_required
def finddoctor():
    doctors = Doctor.query.filter_by(city=current_user.city).all()
    return render_template('doctorlist.html', doclist=doctors)

@app.route('/book/<Did>', methods=['GET', 'POST'])
@login_required
def book(Did):
    app = Appointment(doctor_id=Did, patient_id=current_user.id)
    form = AppointmentForm(obj=app)
    if form.validate_on_submit():
        appoint = Appointment(requested_date=form.date.data, doctor_id=form.doctor_id.data, patient_id=form.patient_id.data, status=0)
        db.session.add(appoint)
        db.session.commit()
        flash('Congratulations, your appointment is successfully booked!')
        return redirect(url_for('home'))
    return render_template('bookdoctor.html', form=form)

@app.route('/myappointments')
@login_required
def myappointments():
    if(current_user.id[0] == 'P'):
        pending_data = Appointment.query.filter_by(patient_id=current_user.id, status=0).all()
        confirmed_data = Appointment.query.filter_by(patient_id=current_user.id, status=1).all()
        rejected_data = Appointment.query.filter_by(patient_id=current_user.id, status=-1).all()
        return render_template('pat_appointment.html', confirm=confirmed_data, pending=pending_data, reject=rejected_data)
    else:
        pending_data = Appointment.query.filter_by(doctor_id=current_user.id, status=0).all()
        confirmed_data = Appointment.query.filter_by(doctor_id=current_user.id, status=1).all()
        #print(pending_data)
        return render_template('doc_appointment.html', confirm=confirmed_data, pending=pending_data)
    

@app.route('/confirmappointment/<aid>', methods=['GET', 'POST'])
@login_required
def confirmappointment(aid):
    app = Appointment.query.filter_by(id=aid).first()
    if(current_user.id[0] == 'P'):
        return redirect(url_for('home'))
    form = confirmAppointment()
    if form.validate_on_submit():
        app.appointment_date = form.appoint_date.data
        app.appointment_time = form.appoint_time.data
        #print(app.appointment_date, app.appointment_time)
        app.status = 1
        db.session.commit()
        return redirect(url_for('myappointments'))
    return render_template('confirm.html', form=form, request = app.requested_date)

@app.route('/rejectappointment/<aid>', methods=['GET', 'POST'])
@login_required
def rejectappointment(aid):
    app = Appointment.query.filter_by(id=aid).first()
    if(current_user.id[0] == 'P'):
        return redirect(url_for('home'))
    form = rejectAppointment()
    if form.validate_on_submit():
        app.reject_msg = form.rejectMessage.data
        app.status = -1
        db.session.commit()
        return redirect(url_for('myappointments'))
    return render_template('reject.html', form=form)

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
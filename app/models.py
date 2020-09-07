from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime 

@login.user_loader
def load_user(id):
    if(id[0] == 'P'):
        return Patient.query.get(id)
    else:
        return Doctor.query.get(id)

class Patient(UserMixin, db.Model):
    id = db.Column(db.String(120), primary_key=True)
    full_name = db.Column(db.String(64), index=True)
    city = db.Column(db.String(20))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(120))
    appointments = db.relationship('Appointment', backref='patient', lazy='dynamic')

    def __repr__(self):
        return '<Patient {}>'.format(self.full_name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Doctor(UserMixin, db.Model):
    id = db.Column(db.String(120), primary_key=True)
    full_name = db.Column(db.String(64), index=True)
    city = db.Column(db.String(20))
    qual = db.Column(db.String(20))
    fees = db.Column(db.Integer)
    phone = db.Column(db.Integer)
    address = db.Column(db.String(120))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(120))
    appointments = db.relationship('Appointment', backref='doctor', lazy='dynamic')

    def __repr__(self):
        return '<Doctor {}>'.format(self.full_name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    requested_date = db.Column(db.Date)
    appointment_date = db.Column(db.Date)
    appointment_time = db.Column(db.Time)
    doctor_id = db.Column(db.String(120), db.ForeignKey('doctor.id'))
    patient_id = db.Column(db.String(120), db.ForeignKey('patient.id'))
    reject_msg = db.Column(db.String(120))
    status = db.Column(db.Integer)
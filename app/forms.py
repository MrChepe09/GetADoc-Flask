from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, Length
from app.models import Doctor, Patient

class LoginForm(FlaskForm):
    choice = SelectField('Are you a Patient or Doctor?', choices=['Patient', 'Doctor'])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log In')

class DoctorRegister(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    phone = IntegerField('Phone No.', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    qual = StringField('Qualifications', validators=[DataRequired()])
    fees = IntegerField('Fees per Person', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        doctor = Doctor.query.filter_by(email=email.data).first()
        if doctor is not None:
            raise ValidationError('Email is already Registered!!')

class PatientRegister(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        patient = Patient.query.filter_by(email=email.data).first()
        if patient is not None:
            raise ValidationError('Email is already Registered!!')


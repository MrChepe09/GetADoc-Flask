from flask import render_template
from app import app
from app.forms import LoginForm, DoctorRegister, PatientRegister

@app.route('/')
def home():
    return render_template('home.html')
    
@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/register/<choice>')
def register(choice):
    if(choice=='doctor'):
        form = DoctorRegister()
    else:
        form = PatientRegister()
    return render_template('register.html', choice=choice, form=form)
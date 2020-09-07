from app import app, db
from app.models import Patient, Doctor, Appointment

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Patient': Patient, 'Doctor': Doctor, 'Appointment': Appointment}
from app import db

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(64), index=True)
    city = db.Column(db.String(20))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(120))

    def __repr__(self):
        return '<Patient {}>'.format(self.full_name)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(64), index=True)
    city = db.Column(db.String(20))
    qual = db.Column(db.String(20))
    fees = db.Column(db.Integer)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(120))

    def __repr__(self):
        return '<Doctor {}>'.format(self.full_name)
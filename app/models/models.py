from flask_sqlalchemy import SQLAlchemy
from app import bcrypt
from app import db


class Staff(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    first_name = db.Column(db.String(50),nullable = False)
    last_name = db.Column(db.String(50),nullable = True)
    email = db.Column(db.String(100),unique = True,nullable = False)
    _password = db.Column(db.String(300),nullable = False)
    role = db.Column(db.String(60),nullable =True, default = 'staff')

    @property
    def password(self):
        raise AttributeError("Cannot Read Passwords")
    
    @password.setter
    def password(self,password):
        self._password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self,password):
        return bcrypt.check_password_hash(self._password,password)
    

class Patients(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    first_name = db.Column(db.String(30),nullable = False)
    last_name = db.Column(db.String(30),nullable = True)
    contact = db.Column(db.String(11),nullable = False)
    email = db.Column(db.String(29),unique = True, nullable = False)
    age = db.Column(db.Integer,nullable = True)
    gender = db.Column(db.String(30),nullable = False)
    blood_group = db.Column(db.String(12),nullable = True)
    medical_history = db.Column(db.Text) 


class Doctors(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    first_name = db.Column(db.String(30),nullable = False)
    last_name = db.Column(db.String(30),nullable = True)
    specs = db.Column(db.String(100))
    contact = db.Column(db.String(100))
    from_time = db.Column(db.Time, nullable = False)
    to_time = db.Column(db.Time,nullable = False)



class Appointments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    a_date = db.Column(db.Date, nullable=False)
    a_time = db.Column(db.Time, nullable=False)
    doctor_first_name = db.Column(db.String(100), nullable=False)
    doctor_last_name = db.Column(db.String(100), nullable=False)
    patient_first_name = db.Column(db.String(100), nullable=False)
    patient_last_name = db.Column(db.String(100), nullable=False)
    patient = db.relationship('Patients', backref='appointments', lazy=True)
    doctor = db.relationship('Doctors', backref='appointments', lazy=True)

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        if self.doctor_id:
            doctor = Doctors.query.get(self.doctor_id)
            self.doctor_first_name = doctor.first_name if doctor else ''
            self.doctor_last_name = doctor.last_name if doctor else ''
        if self.patient_id:
            patient = Patients.query.get(self.patient_id)
            self.patient_first_name = patient.first_name  if patient else ''
            self.patient_last_name = patient.last_name  if patient else ''


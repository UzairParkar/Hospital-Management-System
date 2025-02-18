from flask import Blueprint, request, jsonify
from app import db
from app.models.models import Appointments, Staff, Doctors, Patients
from app.models.schema import appointment_schema, appointments_schema
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

appointments = Blueprint('appointments', __name__, url_prefix='/appointments')


@appointments.route('/create', methods=['POST'])
@jwt_required()
def createappointment():
    staffcred = get_jwt()
    role = staffcred.get('role')

    if role == 'admin':
        return jsonify({"Message": "Only Staff are allowed to manage appointments"}), 403

    if role == 'staff':
        data = request.get_json()
        try:
            patient = Patients.query.get(data['patient_id'])
            doctor = Doctors.query.get(data['doctor_id'])
            if not patient or not doctor:
                return jsonify({"Message": "Invalid patient or doctor ID"}), 404

            appointment = Appointments(
                patient_id=data['patient_id'],
                doctor_id=data['doctor_id'],
                a_date=data['a_date'],
                a_time=data['a_time']
            )
            db.session.add(appointment)
            db.session.commit()
            return appointment_schema.dump(appointment), 200
        except Exception as e:
            return jsonify({'message': str(e)})


@appointments.route('/read', methods=['GET'])
@jwt_required()
def readappointments():
    staffcred = get_jwt()
    role = staffcred.get('role')
    if role == 'admin':
        return jsonify({"Message": "Only Staff are allowed to manage appointments"}), 403

    if role == 'staff':
        appointments_list = Appointments.query.all()
        return appointments_schema.dump(appointments_list), 200


@appointments.route('/read/<int:id>', methods=['GET'])
@jwt_required()
def readappointmentbyid(id):
    staffcred = get_jwt()
    role = staffcred.get('role')
    if role == 'admin':
        return jsonify({"Message": "Only staff are allowed to manage appointments"}), 403

    if id:
        appointment = Appointments.query.get(id)
        if not appointment:
            return jsonify({"Message": "Appointment does not exist"}), 400
        return appointment_schema.dump(appointment), 200


@appointments.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def deleteappointment(id):
    staffcred = get_jwt()
    role = staffcred.get('role')
    if role != 'staff':
        return jsonify({"message": "Only staff can manage appointments"}), 403

    appointment = Appointments.query.get(id)
    if not appointment:
        return jsonify({"message": "Appointment not found"}), 404

    db.session.delete(appointment)
    db.session.commit()
    return jsonify({"message": "Appointment Deleted Successfully"}), 200


@appointments.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
def updateappointment(id):
    staffcred = get_jwt()
    role = staffcred.get('role')
    ddata = request.get_json()

    if role != 'staff':
        return jsonify({'message': "Only staff can manage appointments"}), 403
    else:
        appointment = Appointments.query.get(id)
        if not appointment:
            return jsonify({"message": "Appointment Not Found"}), 404
        appointment.patient_id = ddata.get('patient_id', appointment.patient_id)
        appointment.doctor_id = ddata.get('doctor_id', appointment.doctor_id)
        appointment.a_date = ddata.get('a_date', appointment.a_date)
        appointment.a_time = ddata.get('a_time', appointment.a_time)
        db.session.commit()
        return appointment_schema.dump(appointment), 200

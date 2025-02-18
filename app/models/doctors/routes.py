from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app import db
from app.models.models import Doctors,Staff
from app.models.schema import doctors_schema, doctor_schema

doctors = Blueprint('doctors',__name__,url_prefix="/doctors")

@doctors.route('/create',methods=['POST'])
@jwt_required()
def hiredoctor():
    staffcred = get_jwt()
    role = staffcred.get('role')

    if role != 'admin':
        return jsonify({"Message":"Only admins can manage doctors"}),403
    if role == 'staff':
        required_fields = ['first_name', 'last_name', 'contact', 'from_time', 'to_time', 'specs']
        for field in required_fields:
            if not data.get(field) or data.get(field) == '':
                return jsonify({"Message": f"{field.replace('_', ' ').capitalize()} cannot be empty."}), 400
    else:
        data = request.get_json()
        try:
            doctor = Doctors(
                first_name = data['first_name'],
                last_name = data['last_name'],
                specs = data['specs'],
                contact = data['contact'],
                from_time =data['from_time'],
                to_time = data['to_time']
            )
            db.session.add(doctor)
            db.session.commit()
            return doctor_schema.dump(doctor),200
        except Exception as e:
            return jsonify({'message':str(e)}),404


@doctors.route('/read',methods=['GET'])
@jwt_required()
def readalldoctor():
    staffcred = get_jwt()
    role = staffcred.get('role')
    if role != 'admin':
        return jsonify({'message':"only admins can manage doctors"}),403
    doctor = Doctors.query.all()
    return doctors_schema.dump(doctor),200

@doctors.route('/read/<int:id>',methods=['GET'])
@jwt_required()
def readbyid(id):
    staffcred = get_jwt()
    role = staffcred.get('role')
     
    if role != 'admin':
        return jsonify({"message":"Only admins can handle Doctors"}),403
    
    if id:
        doctor = Doctors.query.get(id)
        if not doctor:
            return jsonify({"message":"Doctor does not exist"}),404
        return doctor_schema.dump(doctor),200

@doctors.route('/update/<int:id>',methods=['PUT'])
@jwt_required()
def updatedoctor(id):
    staffcred = get_jwt()
    role = staffcred.get('role')
    ddata = request.get_json()
    if role != 'admin':
        return jsonify({"message":"only admins can manage doctors"}),403
    else:
        doctor = Doctors.query.get(id)
        if not doctor:
            return jsonify({"message":"Doctor does not exist"}),404
        doctor.first_name = ddata.get('first_name',doctor.first_name)
        doctor.last_name = ddata.get('last_name',doctor.last_name)
        doctor.specs = ddata.get("specs",doctor.specs)
        doctor.contact = ddata.get("contact",doctor.contact)
        doctor.from_time = ddata.get("from_time",doctor.from_time)
        doctor.to_time = ddata.get("to_time",doctor.to_time)
        db.session.commit()
        return doctor_schema.dump(doctor),200
    
@doctors.route('/delete/<int:id>',methods=['DELETE'])
@jwt_required()
def deletepatient(id):
    staffcred = get_jwt()
    role = staffcred.get('role')
    if role != 'admin':
        return jsonify({"message":"Only an admin can fire a doctor"}), 403
    doctor = Doctors.query.get(id)
    if not doctor:
        return jsonify({"Message":"Doctor Does not Exist"}),404
    db.session.delete(doctor)
    db.session.commit()
    return jsonify({"message":"Doctor Deleted"})



     
    

    




        
        


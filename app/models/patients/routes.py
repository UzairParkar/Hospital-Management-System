from flask import Blueprint, request, jsonify
from app import db
from app.models.models import Patients, Staff
from app.models.schema import PatientSchema, patient_schema, patients_schema
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

patients = Blueprint('patients',__name__,url_prefix='/patients')


@patients.route('/create',methods=['POST'])
@jwt_required()
def createpatient():
    staffcred = get_jwt()
    role = staffcred.get('role')

    if role =='admin':
        return jsonify({"Message":"Only Staff are allowed to manage patients"}),403
    

    if role == 'staff':
        data = request.get_json()
        required_fields = ['first_name', 'last_name', 'contact', 'email', 'age', 'gender', 'blood_group', 'medical_history']
        for field in required_fields:
            if not data.get(field) or data.get(field) == '':
                return jsonify({"Message": f"{field.replace('_', ' ').capitalize()} cannot be empty."}), 400
        try:
            patient = Patients(
                first_name = data['first_name'],
                last_name = data['last_name'],
                contact = data['contact'],
                email = data['email'],
                age = data['age'],
                gender = data['gender'],
                blood_group =  data['blood_group'],
                medical_history = data['medical_history']
            )
            db.session.add(patient)
            db.session.commit()
            return patient_schema.dump(patient),200
        except Exception as e:
            return jsonify({'message':str(e)})
        

@patients.route('/read',methods = ['GET'])
@jwt_required()
def readpatient():
    staffcred = get_jwt()
    role = staffcred.get('role')
    if role == 'admin':
        return jsonify({"Message":"Only Staff are allowed to manage patients"}),403
    
    if role == 'staff':
        patient = Patients.query.all()
        return patients_schema.dump(patient),200
    



@patients.route('/read/<int:id>',methods = ['GET'])
@jwt_required()
def readbyid(id):
    staffcred = get_jwt()
    role = staffcred.get('role')
    if role == 'admin':
        return jsonify({"Message":"only staff are allowed to manage patients"}),403
    if id:
        patient = Patients.query.get(id)
        if not patient:
            return jsonify({"Message":"Patient does not exist"}),400
        return patient_schema.dump(patient),200
    
    
@patients.route('/delete/<int:id>',methods=['DELETE'])
@jwt_required()
def deletepatient(id):
    staffcred = get_jwt()
    role = staffcred.get('role')
    if role != 'staff':
        return jsonify({"message":"Only staff can manage patients"}), 403
    
    patient = Patients.query.get(id)
    if not patient:
        return jsonify({"message":"Patient not found"}),404
    
    db.session.delete(patient)
    db.session.commit()
    return jsonify({"message":"Patient Deleted Sucessfully"}),200

@patients.route('/update/<int:id>',methods=['PUT'])
@jwt_required()
def updatepatient(id):
    staffcred = get_jwt()
    role = staffcred.get('role')
    ddata = request.get_json()
    
    if role != 'staff':
        return jsonify({'message':"Only staff can manage patients"}),403
    else:
        patient = Patients.query.get(id)
        if not patient:
            return jsonify({"message":"Patient Not Found"}),404
        patient.first_name = ddata.get('first_name',patient.first_name)
        patient.last_name = ddata.get('last_name',patient.last_name)
        patient.contact = ddata.get('contact',patient.contact)
        patient.email = ddata.get('email',patient.email)
        patient.age = ddata.get('age',patient.age)
        patient.gender = ddata.get('gender',patient.gender)
        patient.blood_group = ddata.get('blood_group',patient.blood_group)
        patient.medical_history = ddata.get('medical_history',patient.medical_history)
        db.session.commit()
        return patient_schema.dump(patient),200


    
    




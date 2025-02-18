from flask import Blueprint, request, make_response, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models.models import Staff
from app.models.schema import staff_schema, staffs_schema
from app import db

staff = Blueprint('staff',__name__,url_prefix='/staff')


@staff.route('/read',methods=['GET'])
@jwt_required()
def readall():
    staffcred = get_jwt()
    if staffcred.get("role") != "admin":
        return jsonify({'message':"cannot perform that function"}),403
    else:
        staff = Staff.query.all()
        return staffs_schema.dump(staff),200


@staff.route('/read/<int:id>',methods=['GET'])
@jwt_required()
def readbyid(id):
    staffcred = get_jwt()
    if staffcred.get('role') != 'admin':
        return jsonify({"Message":"Cannot Pefrom that function"}),403
    if id:
        staff = Staff.query.get(id)
        if not staff:
            return jsonify({"Message":"Staff does not exist"}),400
        return staff_schema.dump(staff),200
    

@staff.route('/update/<int:id>',methods=['PUT'])
@jwt_required()
def updatestaff(id):
    current_user = get_jwt_identity()
    ddata = request.get_json()
    if int(current_user) != id:
        return jsonify({"message":"You can only make changes yo your own profile"}), 403
    else:
        staff = Staff.query.get(id)
        if not staff:
            return jsonify({'message':"staff not found"}), 404
        staff.first_name = ddata.get('first_name',staff.first_name)
        staff.last_name = ddata.get('last_name',staff.last_name)
        staff.email = ddata.get('email',staff.email)

        if 'password' in ddata:
            staff.password = ddata['password']

            db.session.commit()
            return staff_schema.dump(staff),200
        

@staff.route('/delete/<int:id>',methods=['DELETE'])
@jwt_required()
def deletestaff(id):
    staffcred = get_jwt()
    role = staffcred.get('role')
    if role != 'admin':
        return jsonify({"message":"Only Admins are allowed to fire Staff"}), 403
    
    staff = Staff.query.get(id)
    if not staff:
        return jsonify({"message":"Staff not found"}),404
    db.session.delete(staff)
    db.session.commit()
    return jsonify({"message":"Staff Deleted Sucessfully"}),200


        
        
        

    
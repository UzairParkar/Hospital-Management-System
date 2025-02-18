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
    
@staff.route('/update', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user = get_jwt_identity()
    ddata = request.get_json()
    staff = Staff.query.get(current_user) 

    if not staff:
        return jsonify({'message': "Staff not found"}), 404

    staff.first_name = ddata.get('first_name', staff.first_name)
    staff.last_name = ddata.get('last_name', staff.last_name)
    staff.email = ddata.get('email', staff.email)

    if 'password' in ddata and ddata['password'].strip():
        staff.password = ddata['password']

    db.session.commit()
    return staff_schema.dump(staff), 200

@staff.route('/make_admin/<int:id>', methods=['PUT'])
@jwt_required()
def make_admin(id):
    current_user = get_jwt_identity()
    staffcred = get_jwt()
    role = staffcred.get('role')

    staff = Staff.query.get(id)
    if not staff:
        return jsonify({'message': "Staff not found"}), 404
    
    if current_user != '1':
        print(current_user)
        return jsonify({"message": "Only super admin can promote staff to admin"}), 403

    staff.role = 'admin'
    db.session.commit()
    return staff_schema.dump(staff), 200

@staff.route('/demote/<int:id>', methods=['PUT'])
@jwt_required()
def demote_admin(id):
    current_user = get_jwt_identity()

    staff = Staff.query.get(id)
    if not staff:
        return jsonify({'message': "Admin not found"}), 404

    if staff.role != 'admin':
        return jsonify({"message": "This user is not an admin"}), 400
    
    if staff.id == 1:
        return jsonify({"message":"cannot demote a super admin"}),403
    
    if current_user != '1':
        return jsonify({"message": "Only super admin can demote admins"}), 403
    

    staff.role = 'staff'
    db.session.commit()
    return staff_schema.dump(staff), 200



@staff.route('/delete/<int:id>',methods=['DELETE'])
@jwt_required()
def deletestaff(id):
    current_user = get_jwt_identity()
    staffcred = get_jwt()
    role = staffcred.get('role')
    if role != 'admin':
        return jsonify({"message":"Only Admins are allowed to fire Staff"}), 403
    
    staff = Staff.query.get(id)
    if not staff:
        return jsonify({"message":"Staff not found"}),404
    
    if staff.id ==1:
        return jsonify({"message": "Super admin cannot be fired"}), 403
    
    db.session.delete(staff)
    db.session.commit()
    return jsonify({"message":"Staff Deleted Sucessfully"}),200


        
        
        

    

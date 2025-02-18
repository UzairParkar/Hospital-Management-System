from flask import Blueprint,request,jsonify
from app.models.models import Staff
from app.models.schema import staff_schema
from app import db
from flask_jwt_extended import jwt_required, set_access_cookies, create_access_token, unset_access_cookies, get_jwt_identity
from datetime import timedelta


auth = Blueprint("auth",__name__,url_prefix='/auth')


@auth.route('/register',methods=['POST'])
def register():
    data_in = request.json
    data_in['role'] ='staff'
    try:
        ddata = staff_schema.load(data_in)
    except Exception as err:
        return jsonify({'message':str(err)}),400
    
    if Staff.query.filter_by(email=ddata['email']).first():
        return jsonify({"Message":"Staff member already exists --Try Logging in"}),400
    


    new_staff = Staff(
        first_name = ddata['first_name'],
        last_name = ddata['last_name'],
        email = ddata['email'],
        role = ddata['role']

    ) 
    new_staff.password = ddata['password']
    db.session.add(new_staff)
    db.session.commit()
    
    return jsonify({"Message":"Staff Registered successfully"}),201



@auth.route('/login',methods=['POST'])
def login():
    ddata = request.get_json()
    email = ddata.get('email')
    password = ddata.get('password')

    if not email or not password:
        return {'message': 'Email and password are required'}, 400

    
    staff = Staff.query.filter_by(email=ddata['email']).first()

    if not staff or not staff.verify_password(password):
         return jsonify({"Message":'invalid credentials'}), 404
    
    else:
        token = create_access_token(identity= str(staff.id),
            additional_claims={'role':staff.role,'email':email},expires_delta=timedelta(minutes=5))
        
        response = jsonify(token)
        set_access_cookies(response,token)
        return response,200

    




@auth.route('/logout',methods = ['POST'])
@jwt_required()
def logout():
    response = jsonify({'message':"successfully logged out"})
    unset_access_cookies(response)
    return response,200









    
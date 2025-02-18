from marshmallow import Schema, fields, validate


class StaffSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    role = fields.Str(required=True, validate=validate.OneOf(['staff', 'admin']))


class PatientSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    blood_group = fields.Str(required=True,validate=validate.OneOf(['A+','A-','B+','B-','AB+','AB-','O+','O-']))
    age = fields.Int(required=True)
    email = fields.Email(required=True)
    gender = fields.Str(required=True, validate=validate.OneOf(['Male', 'Female', 'Other']))
    contact = fields.Str(required=True)
    medical_history = fields.Str()

class DoctorSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    specs = fields.Str(required=True)
    contact = fields.Str(required=True)
    from_time = fields.Time(required=True)
    to_time = fields.Time(required=True)

class AppointmentSchema(Schema):
    id = fields.Int(dump_only=True)
    patient_id = fields.Int(required=True)
    doctor_id = fields.Int(required=True)
    a_date = fields.Date(required=True)
    a_time = fields.Time(required=True)

staff_schema = StaffSchema()
staffs_schema = StaffSchema(many=True)

patient_schema = PatientSchema()
patients_schema = PatientSchema(many=True)

doctor_schema = DoctorSchema()
doctors_schema = DoctorSchema(many=True)

appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many=True)
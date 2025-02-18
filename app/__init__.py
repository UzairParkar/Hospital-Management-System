from flask import Flask
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from flask_bcrypt import Bcrypt

ma = Marshmallow()
db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()


def create_app():
    global app
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    create_def_admin()
    CORS(app,supports_credentials=True)
    from app.auth.routes import auth
    from app.models.appointments.routes import appointments
    from app.models.staff.routes import staff
    from app.models.patients.routes import patients
    from app.models.doctors.routes import doctors

    app.register_blueprint(auth)
    app.register_blueprint(appointments)
    app.register_blueprint(staff)
    app.register_blueprint(patients)
    app.register_blueprint(doctors)


    return app


def create_def_admin():
    with app.app_context():
        from app.models.models import Staff
        admin = Staff.query.filter_by(role='admin').first()
        if not admin:
            admin = Staff(first_name=app.config["DEFAULT_ADMIN_NAME"], last_name = app.config["DEFAULT_ADMIN_LAST_NAME"],email=app.config["DEFAULT_ADMIN_EMAIL"], role="admin")
            admin.password = app.config['DEFAULT_ADMIN_PASSWORD']
            db.session.add(admin)
            db.session.commit()



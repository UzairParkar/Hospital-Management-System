
# Hospital Management System 

```
Overview
```

**Hospital Management System is an API that follows the standards of the REST architectural Style.**

### ⚙️ Features of the API
- Uniform Interface
- Modular Structure
- Authorized and Authenticated
- Role Based Access Control 
- Error Tested

### 📦TechStack
- Flask (Python-Web-FrameWork)
- SQLAlchemy (Object Relational Mapper)
- Alembic(Database Migration Tool)
- Flask-JWT-Extended (Authentication)
- Postgresql (Database)
- POSTMAN (API testing tool)

### 🔀 Clone The Repository
```
git clone  https://github.com/UzairParkar/Hospital-Management-System.git

```

### Create a virtual Environment

```
virtualenv env
```

### activate the Environment
```
env\Scripts\activate.ps1
```

### 🗄️ Installing Dependencies

```
pip install -r requirements.txt
```

### ⚡More info

```
Here is some more information about the API
before you begin exploring it more i have
also listed down a list of views so that it
becomes easier for you to test it.
```

### How it works

-> When the app runs for the first time an admin is added automatiucally into the databse as the super admin, this admin manages staff and doctors.

-> The second level of authority is staff
that manage patients and appointments.

-> Marshmallow looks over the schema validation and manages fields such as blood group and genders. 

-> This Api also checks for empty fields and authorizatiion when updating admins and staff with higher roles. 

Here a list of the views so that it becomes easier for you to interact with the code

```
Endpoint                 Methods  Rule
-----------------------  -------  -----------------------------
appointments.create      POST     /appointments/create
appointments.delete_app  DELETE   /appointments/delete/<int:id>
appointments.read_app    GET      /appointments/read
appointments.read_by_id  GET      /appointments/read/<int:id>  
appointments.update_app  PUT      /appointments/update/<int:id>
auth.login               POST     /auth/login
auth.logout              POST     /auth/logout
auth.register            POST     /auth/register
doctors.deletepatient    DELETE   /doctors/delete/<int:id>
doctors.hiredoctor       POST     /doctors/create
doctors.readalldoctor    GET      /doctors/read
doctors.readbyid         GET      /doctors/read/<int:id>
doctors.updatedoctor     PUT      /doctors/update/<int:id>
patients.createpatient   POST     /patients/create
patients.deletepatient   DELETE   /patients/delete/<int:id>
patients.readbyid        GET      /patients/read/<int:id>
patients.readpatient     GET      /patients/read
patients.updatepatient   PUT      /patients/update/<int:id>
staff.deletestaff        DELETE   /staff/delete/<int:id>
staff.demote_admin       PUT      /staff/demote/<int:id>
staff.make_admin         PUT      /staff/make_admin/<int:id>
staff.readall            GET      /staff/read
staff.readbyid           GET      /staff/read/<int:id>
staff.update_profile     PUT      /staff/update
static                   GET      /static/<path:filename>
```

```
🎓 If you have any suggestions for better and more efficient code,
i am all ears raise it in the issue and i'll get it fixed`
```









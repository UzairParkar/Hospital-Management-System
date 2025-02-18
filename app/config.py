class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:root@localhost:5432/project1'
    SLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'yektercesa'
    DEFAULT_ADMIN_NAME = "SUPER_ADMIN"
    DEFAULT_ADMIN_LAST_NAME = "007"
    DEFAULT_ADMIN_EMAIL = "Admin.hospital@gmail.com"
    DEFAULT_ADMIN_PASSWORD = "tercesdrowssap"
    JWT_TOKEN_LOCATION = 'cookies'
    JWT_ACCESS_COOKIE_PATH ='/'
    JWT_COOKIE_CSRF_PROTECT = False
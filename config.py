from secret import db_user, db_password, db_name, secret_key
class Conf:
    UPLOAD_FOLDER = "static/uploads/"
    SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_password}@localhost:5432/{db_name}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AUTO_RELOAD_TEMPLATES = True
    SECRET_KEY = secret_key
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    SEND_FILE_MAX_AGE_DEFAULT = 0
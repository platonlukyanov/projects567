from secret import db_user, db_password, db_name
class Conf:
    UPLOAD_FOLDER = "static/uploads/"
    SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_password}@localhost:5432/{db_name}"
    AUTO_RELOAD_TEMPLATES = True
    DEBUG = True
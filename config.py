from secret import db_user, db_password, db_name, secret_key


class Conf:
    PROJECT_TITLE_IMAGE_FOLDER = "static/uploaded-images/projects_titles"
    IMAGE_ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "svg", "gif", "webp"]
    UPLOAD_FOLDER = "static/uploads/"
    # SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_password}@localhost:5432/{db_name}"

    SQLALCHEMY_DATABASE_URI = f"sqlite:///data.db?check_same_thread=False"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AUTO_RELOAD_TEMPLATES = True
    SECRET_KEY = secret_key
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    SEND_FILE_MAX_AGE_DEFAULT = 0

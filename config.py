from secret import db_user, db_password, db_name, secret_key, m_username, m_password, m_default_sender, conf_salt


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
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = m_username
    MAIL_PASSWORD = m_password
    MAIL_DEFAULT_SENDER = m_default_sender
    CONFIRMATION_SALT = conf_salt
import os

secret_key = os.getenv("SECRET")
conf_salt = os.getenv("SALT")

m_password = os.getenv("MAIL_PASSWORD")
m_username = os.getenv("MAIL_USERNAME")
m_default_sender = os.getenv("MAIL_DEFAULT_SENDER")

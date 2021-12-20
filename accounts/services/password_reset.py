from models import *
from itsdangerous import JSONWebSignatureSerializer as Serializer
from app import app


def get_reset_token(user_id):
    s = Serializer(app.config["SECRET_KEY"], 'email_conf')
    return s.dumps({"user_id": user_id})


def verify_reset_token(token):
    s = Serializer(app.config["SECRET_KEY"], 'email_conf')
    try:
        user_id = s.loads(token)["user_id"]
    except:
        return
    return User.query.get(user_id)

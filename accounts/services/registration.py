from models import *
from werkzeug.security import generate_password_hash


def register_new_user(form):
    new_user = User()
    new_user.email = form.email.data
    new_user.password = generate_password_hash(form.password.data)
    usertype = int(form.usertype.data)  # id
    new_user.usertype = UserType.query.filter(UserType.id == usertype).first()
    new_user.first_name = form.first_name.data
    new_user.last_name = form.last_name.data
    ss = db.session
    ss.add(new_user)
    ss.commit()
    return new_user


def confirm_user_registration(email):
    user = User.query.filter_by(email=email).first()
    user.email_confirmed = True
    db.session.commit()

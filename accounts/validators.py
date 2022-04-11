from werkzeug.security import check_password_hash
from wtforms import PasswordField, Field, Form
from wtforms.validators import ValidationError
from models import *


class ConfirmedEmailValidator(object):

    def __init__(self, message: str = ""):
        if not message:
            message = 'Электронная почта не подтверждена'
        self.message = message

    def __call__(self, form, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            if not user.email_confirmed:
                raise ValidationError(self.message)


class RightUserPasswordValidator(object):

    def __init__(self, message: str = "", email_field: str = "email"):
        if not message:
            message = 'Неверный пароль'
        self.message = message
        self.email_field = email_field

    def __call__(self, form, field):
        user = User.query.filter_by(email=getattr(form, self.email_field).data).first()
        if user:
            if not check_password_hash(user.password, field.data):
                raise ValidationError(self.message)


class ExistUserValidator(object):

    def __init__(self, message: str = ""):
        if not message:
            message = 'Пользователя с такой электронной почтой не существует'
        self.message = message

    def __call__(self, form, field):
        user = User.query.filter_by(email=field.data).first()
        if not user:
            raise ValidationError(self.message)


class PasswordEquality(object):
    def __init__(self, message: str = "", second_password_attr: str = "password2"):
        if not message:
            message = 'Введеные пароли не одинаковые'
        self.message = message
        self.second_password_attr = second_password_attr

    def __call__(self, form: Form, field: Field):

        if field.data != getattr(form, self.second_password_attr).data:
            raise ValidationError(self.message)

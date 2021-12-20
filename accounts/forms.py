from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired
from form_widgets import *
from accounts.validators import *


class RegisterForm(FlaskForm):
    first_name = StringField("Имя и фамилия: ", widget=VerifyText(),
                             validators=[InputRequired(message="Заполните поле имени")])
    last_name = StringField('last_name', widget=VerifyText(),
                            validators=[InputRequired(message="Заполните поле фамилии")])
    email = StringField("Эл. Почта: ", widget=VerifyEmail(),
                        validators=[InputRequired(message="Заполните поле пароля")])
    usertype = RadioField('Тип пользователя: ', choices=[[str(i[0]), i[1]] for i in
                                                         UserType.query.with_entities(UserType.id,
                                                                                      UserType.name).all()],
                          validators=[InputRequired(message="Заполните поле выбора типа пользователя")])

    password2 = PasswordField("Повторите пароль: ", widget=VerifyPassword(),
                              validators=[InputRequired(message="Заполните поле подтверждения пароля")])
    password = PasswordField("Пароль: ", widget=VerifyPassword(),
                             validators=[InputRequired(message="Заполните поле пароля"),
                                         PasswordEquality(second_password_attr='password2')])


class LoginForm(FlaskForm):
    email = StringField("Эл. Почта: ", validators=[InputRequired(message="Заполните поле пароля"), ExistUserValidator(),
                                                   ConfirmedEmailValidator()], widget=VerifyEmail())
    password = PasswordField("Пароль: ",
                             validators=[InputRequired(message="Заполните поле пароля"),
                                         RightUserPasswordValidator()], widget=VerifyPassword())
    remember_me = BooleanField("Запомнить меня")


class EmailFormResetPassword(FlaskForm):
    email = EmailField('Электронная почта', validators=[InputRequired(message="Заполните поле пароля"), ExistUserValidator(),
                       ConfirmedEmailValidator()], widget=VerifyEmail())


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Новый пароль: ",
                             validators=[InputRequired(message="Заполните поле пароля"), PasswordEquality()],
                             widget=VerifyPassword())
    password2 = PasswordField("Повторите пароль: ",
                              validators=[InputRequired(message="Заполните поле подтверждения пароля")], widget=VerifyPassword())

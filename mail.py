from flask_mail import Mail, Message
from flask import render_template, url_for
from app import app
from models import *

mail = Mail(app)


# @app.route('/send-mail')
# def send_mail():
#     users = User.query.all()
#     with mail.connect() as conn:
#         for user in users:
#             msg = Message('Some email', recipients=[user.email])
#             msg.html = render_template("mail/mail.html", user=user)
#             conn.send(msg)
#     return "succes!"


def send_confirm_email(token, user):
    msg = Message('Подтверждение Электронной почты', recipients=[user.email])
    link = url_for('confirm_email', token=token, _external=True)
    msg.html = render_template("mail/confirm_email.html", user=user, link=link)
    mail.send(msg)


def send_reset_password_email(token, user):
    msg = Message('Подтверждение Электронной почты', recipients=[user.email])
    link = url_for('reset_password', token=token, _external=True)
    msg.html = render_template("mail/reset_password.html", user=user, link=link)
    mail.send(msg)

from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash
from itsdangerous import URLSafeTimedSerializer, BadTimeSignature
from flask import Blueprint
from flask import render_template, request, url_for, redirect, flash
from mail import send_confirm_email, send_reset_password_email
from accounts.forms import RegisterForm, EmailFormResetPassword, ResetPasswordForm, LoginForm
from accounts.services.password_reset import *
from accounts.services.registration import register_new_user, confirm_user_registration

accounts = Blueprint('accounts', __name__, template_folder="templates/accounts")
s = URLSafeTimedSerializer(app.config["SECRET_KEY"])


@accounts.route("/confirm-email/<token>")
def confirm_email(token):
    try:
        email = s.loads(token, salt=app.config["CONFIRMATION_SALT"], max_age=3600)
    except BadTimeSignature:
        return "Срок подтверждение электронной почты истек"
    confirm_user_registration(email)
    return f"адрес электронной почты {email} был подтвержден"


@accounts.route('/login', methods=["GET", "POST"])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        remember = form.remember_me.data
        user = User.query.filter_by(email=email).first()
        login_user(user, remember=remember)
        next_page = request.args.get('next')
        return redirect(next_page if next_page else '/')

    all_subjects = Subject.query.all()
    return render_template('login.html', subjects=all_subjects, form=form)


@accounts.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = register_new_user(form)
        token = s.dumps(new_user.email, salt=app.config["CONFIRMATION_SALT"])
        send_confirm_email(token, new_user)
        flash("Письмо подтверждения аккаунта было отправлено вам на почту, для того чтобы вы могли войти в аккаунт",
              'info')
        return redirect(url_for('accounts.login_page'))
    print(form.data)
    all_subjects = Subject.query.all()
    return render_template('register.html', subjects=all_subjects, form=form)


@accounts.route("/reset-password", methods=["GET", "POST"])
def reset_password_email():
    form = EmailFormResetPassword()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        token = get_reset_token(user.id)
        send_reset_password_email(token, user)
        flash('Письмо для сброса пароля было отправлено вам на почту', 'info')
        return redirect(request.url)
    all_subjects = Subject.query.all()
    return render_template("reset_password_email.html", subjects=all_subjects, form=form)


@accounts.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = verify_reset_token(token)
        if not user:
            flash("Неправильная или истекшая ссылка", 'danger')
            return redirect(request.url)
        user.password = generate_password_hash(form.password.data)
        db.session.commit()
        return redirect(url_for('accounts.login_page'))
    all_subjects = Subject.query.all()
    return render_template('reset_password.html', subjects=all_subjects, form=form)


@accounts.route('/logout', methods=["GET", "POST"])
def logout():
    logout_user()
    next_page = request.args.get('next')
    return redirect(next_page if next_page else '/')


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('accounts.login_page') + "?next=" + request.url)
    return response

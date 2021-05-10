from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import URLSafeTimedSerializer, BadTimeSignature, BadSignature
from app import db, app
from flask import render_template, request, url_for, redirect, flash
from models import *
from mail import send_confirm_email, send_reset_password_email

s = URLSafeTimedSerializer(app.config["SECRET_KEY"])


@app.route("/confirm-email/<token>")
def confirm_email(token):
    try:
        email = s.loads(token, salt=app.config["CONFIRMATION_SALT"], max_age=3600)
    except BadTimeSignature:
        return "Срок подтверждение электронной почты истек"
    user = User.query.filter_by(email=email).first()
    user.email_confirmed = True
    db.session.commit()
    return f"адрес электронной почты {email} был подтвержден"


@app.route('/login', methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        if email and password:
            user = User.query.filter_by(email=email).first()

            if user and check_password_hash(user.password, password):
                if user.email_confirmed:
                    remember = request.form.get('remember')

                    login_user(user, remember=bool(remember))

                    next_page = request.args.get('next')

                    return redirect(next_page if next_page else '/')
                else:
                    flash('Адрес электронной почты не подтвержден')

            else:
                flash('Некорректные пароль или адрес электронной почты')
        else:
            flash('Введите логин и пароль')
            return render_template('login.html')
    all_subjects = Subject.query.all()
    return render_template('login.html', subjects=all_subjects)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        password2 = request.form.get('password2', '')
        usertype = request.form.get('usertype', '')  # id
        first_name = request.form.get('first_name', '')
        last_name = request.form.get('last_name', '')
        tmp = 0
        if not (email or password or password2 or first_name or last_name or usertype):
            flash('Заполните обязательные поля')
            tmp += 1
        if password2 != password:
            flash('Введенные пароли не совпадают')
            tmp += 1
        if tmp > 0:
            return render_template('register.html', password=password, email=email, first_name=first_name,
                                   last_name=last_name, usertype=usertype)
        else:
            token = s.dumps(email, salt=app.config["CONFIRMATION_SALT"])
            hash_pwd = generate_password_hash(password)
            usertype = UserType.query.filter(UserType.id == usertype).first()
            new_user = User(first_name=first_name, last_name=last_name, email=email, password=hash_pwd,
                            usertype=usertype)
            ss = db.session
            ss.add(new_user)
            ss.commit()
            send_confirm_email(token, new_user)
            flash("Письмо подтверждения аккаунта было отправлено вам на почту, для того чтобы вы могли войти в аккаунт",
                  'info')
            return redirect(url_for('login_page'))

    usertypes = UserType.query.filter(UserType.slug != "admin").all()
    all_subjects = Subject.query.all()
    return render_template('register.html', usertypes=usertypes, subjects=all_subjects)


@app.route("/reset-password", methods=["GET", "POST"])
def reset_password_email():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form.get("email")).first()
        if not user:
            flash("Пользователя с данным адресом электронной почты не существует", 'warning')
            return redirect(request.url)
        token = user.get_reset_token()
        send_reset_password_email(token, user)
        flash('Письмо для сброса пароля было отправлено вам на почту')
        return redirect(request.url)
    all_subjects = Subject.query.all()
    return render_template("reset_password_email.html", subjects=all_subjects)


@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if request.method == "POST":
        print('a_am_hear')
        user = User.verify_reset_token(token)
        if not user:
            flash("Неправильная или истекшая ссылка", 'danger')
            return redirect(request.url)
        user.password = generate_password_hash(request.form.get("password"))
        db.session.commit()
        print(user)
        return redirect(url_for('login_page'))
    all_subjects = Subject.query.all()
    return render_template('reset_password.html', subjects=all_subjects)


@app.route('/logout', methods=["GET", "POST"])
def logout():
    logout_user()
    next_page = request.args.get('next')
    return redirect(next_page if next_page else '/')


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + "?next=" + request.url)
    return response

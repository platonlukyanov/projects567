from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, app
from flask import render_template, request, url_for, redirect, flash
from models import *


@app.route('/login', methods=["GET", "POST"])
def login_page():
    email = request.form.get('email')
    password = request.form.get('password')
    if email and password:
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)

            next_page = request.args.get('next')

            return redirect(next_page if next_page else '/')

        else:
            flash('Некорректные пароль или адрес электронной почты')
    else:
        flash('Введите логин и пароль')
        return render_template('login.html')


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

            hash_pwd = generate_password_hash(password)
            usertype = UserType.query.filter(UserType.id == usertype).first()
            new_user = User(first_name=first_name, last_name=last_name, email=email, password=hash_pwd,
                            usertype=usertype)
            ss = db.session
            ss.add(new_user)
            ss.commit()

            return redirect(url_for('login_page'))

    usertypes = UserType.query.filter(UserType.slug != "admin").all()
    return render_template('register.html', usertypes=usertypes)


@app.route('/logout', methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect('/')


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + "?next=" + request.url)
    return response

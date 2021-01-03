from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from app import db
from .forms import LoginForm, Registration

authentication = Blueprint('authentication', __name__)


# Login
@authentication.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        name = form.name.data
        password = form.password.data
        remember = form.checkbox.data
        user = User.query.filter_by(name=name).first()
        if not user or not check_password_hash(user.password, password):
            flash('<div class="alert alert-danger">Некорректное имя пользователя или пароль</div>')
            return redirect(url_for('authentication.login'))
        login_user(user, remember=remember)
        return redirect(url_for('storage.directories'))
    elif request.method == 'GET':
        return render_template('authentication/login.html', title='Вход', form=form)
    else:
        return 'Ошибка. Обратитесь к администратору.'


# Signup
@authentication.route('/signup', methods=['POST', 'GET'])
def signup():
    form = Registration()
    if request.method == 'POST':
        name = form.username.data
        user = User.query.filter_by(name=name).first()
        # checking for already exist user with current name
        if user:
            flash('<div class="alert alert-danger">Не удалось зарегистрировать пользователя. '
                  'Пользователь с таким именем уже существует.</div>')
            return redirect(url_for('authentication.signup'))
        # checking for main conditions
        password = form.password.data
        password_repeat = form.password_repeat.data
        try:
            if len(name) > 4 and len(password) > 4 and password == password_repeat:
                password_hash = generate_password_hash(password)
                user = User(name=name, password=password_hash)
                # Delete @ for role create
                name_to_registration = user.role_name()
                # Role creation by default user, which can only create users and give them default roles
                db.session.add(user)
                db.session.execute(f'CREATE USER {name_to_registration} WITH PASSWORD :password',
                                            {'password': user.password})
                db.session.execute(f'GRANT user_role TO {name_to_registration}')
                db.session.commit()
                flash('<div class="alert alert-success">Регистрация прошла успешно.</div>')
                return redirect(url_for('authentication.login'))
            elif password != password_repeat:
                flash('<div class="alert alert-danger">Пароли не совпадают.</div>')
                return redirect(url_for('authentication.signup'))
            else:
                flash('<div class="alert alert-danger">Не удалось зарегистрировать пользователя. '
                      'Длина пароля и имени должна быть не менее 5 символов</div>')
                return redirect(url_for('authentication.signup'))
        except:
            db.session.rollback()
            flash('<div class="alert alert-danger">Не удалось зарегистрировать пользователя. '
                  'Попробуйте еще раз или обратитесь к администратору</div>')
            return redirect(url_for('authentication.signup'))
    # if user want to signup
    elif request.method == 'GET':
        return render_template('authentication/signup.html', title='Регистрация', form=form)
    else:
        return 'Ошибка, обратитесь к администратору'


# Logout
@authentication.route('/logout')
@login_required
def logout():
    logout_user()
    flash('<div class="alert alert-danger">Вы вышли из личного кабинета.</div>')
    return redirect(url_for('authentication.login'))

# Profile. Nothing inside yet
@authentication.route('/profile')
@login_required
def profile():
    user = current_user
    return render_template('authentication/profile.html', title='Мой профиль', user=user)
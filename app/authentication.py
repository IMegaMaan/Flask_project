from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from app import db

# from flask import jsonify  # work with json

authentication = Blueprint('authentication', __name__)


# Login
@authentication.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        name = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(name=name).first()
        if not user or not check_password_hash(user.password, password):
            flash('<div class="alert alert-danger">Некорректное имя пользователя или пароль</div>')
            return redirect(
                url_for('authentication.login'))
        login_user(user, remember=remember)
        return redirect(url_for('storage.directories'))
    elif request.method == 'GET':
        return render_template('authentication/login.html', title='Вход')
    else:
        return 'Ошибка. Обратитесь к администратору.'


# Signup
@authentication.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        name = request.form['username']
        user = User.query.filter_by(name=name).first()
        # checking for already exist user with current name
        if user:
            flash('<div class="alert alert-danger">Не удалось зарегистрировать пользователя. '
                  'Пользователь с таким именем уже существует.</div>')
            return redirect(url_for('authentication.signup'))
        # checking for main conditions
        try:
            if len(name) > 4 and len(request.form['password']) > 4 and \
                    request.form['password'] == request.form['password_repeat']:
                password_hash = generate_password_hash(request.form['password'])
                user = User(name=name, password=password_hash)
                db.session.add(user)
                db.session.commit()
                flash('<div class="alert alert-success">Регистрация прошла успешно.</div>')
                return redirect(url_for('authentication.login'))
            else:
                flash('<div class="alert alert-danger">Не удалось зарегистрировать пользователя. '
                      'Длина пароля и имени должна быть не менее 5 символов</div>')
                return redirect(url_for('authentication.signup'))
        # exceptions
        except:
            flash('<div class="alert alert-danger">Не удалось зарегистрировать пользователя. '
                  'Попробуйте еще раз или обратитесь к администратору</div>')
            return redirect(url_for('authentication.signup'))
    # if user want to signup
    elif request.method == 'GET':
        return render_template('authentication/signup.html', title='Регистрация')
    else:
        return 'Ошибка, обратитесь к администратору'


# Logout
@authentication.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('storage.index'))

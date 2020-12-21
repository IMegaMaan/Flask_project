from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import os
from app import db
from .models import Directories, UploadedFiles
import shutil

# from flask import jsonify  #for work with json

storage = Blueprint('storage', __name__)


# Home page
@storage.route('/')
def index():
    return render_template('storage/index.html', title='Домашняя страница')


# Create directory
# Only for registered users
@storage.route('/create_directory', methods=['POST', 'GET'])
@login_required
def create_directory():
    if request.method == 'POST' and request.form['name'] != '':  # если пользователь отправляет даные методом POST
        name = request.form['name']
        description = request.form['description']
        directory = Directories(name=name, description=description, user_id_value=current_user.id)
        try:
            # Save to Data Base
            db.session.add(directory)
            db.session.commit()
            # Create directory
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads', str(directory.id))
            os.makedirs(path)
            return redirect('/create_directory')
        except:
            return 'Не удалось создать директорию!'
    elif request.method == 'GET':
        return render_template('storage/create_directory.html', title='Создание директории')
    else:
        return 'Некорректное создание формы'


# Directories views
@storage.route('/directories')
@login_required
def directories():
    db_directories = Directories.query.order_by(Directories.date).filter_by(user_id_value=current_user.id).all()
    total_directories = []
    stop = 0
    while stop < len(list(db_directories)):
        start = stop
        stop += 3
        total_directories.append(db_directories[start:stop:1])
    db_directories = total_directories
    return render_template('storage/directories.html', title='Хранилище файлов', db_directories=db_directories)


# One directory view
@storage.route('/directory/<int:id>', methods=['POST', 'GET'])
@login_required
def directory(id):
    db_all_directories = Directories.query.order_by(Directories.date).filter_by(user_id_value=current_user.id).all()
    db_directories = Directories.query.get(id)
    db_files = UploadedFiles.query.filter_by(parent_id_value=id).all()
    try:
        db_files = UploadedFiles.query.filter_by(parent_id_value=id).all()
    except:
        return 'Произошла ошибка'
    return render_template('storage/directory.html', title=db_directories.name, db_directories=db_directories,
                           db_files=db_files, db_all_directories=db_all_directories)


# Delete the directory and all files inside
@storage.route('/directory/delete/<int:id>')
@login_required
def directory_delete(id):
    db_directories = Directories.query.get_or_404(id)
    try:
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads', str(id))
        shutil.rmtree(path)
        children_files = UploadedFiles.query.filter_by(parent_id_value=id).all()
        # delete information with related files
        for record in children_files:
            db.session.delete(record)
        # delete information about parent directory
        db.session.delete(db_directories)
        db.session.commit()
        return redirect('/directories')
    except:
        return 'Не удалось удалить файл'


# Change Name and Description of Directory
@storage.route('/directory/update/<int:id>', methods=['POST', 'GET'])
@login_required
def directory_update(id):
    db_directories = Directories.query.get_or_404(id)
    if request.method == 'POST':
        db_directories.name = request.form['name']
        db_directories.description = request.form['description']
        try:
            db.session.commit()
            id = db_directories.id
            home_redirect = '/directory/' + str(id)
            return redirect(home_redirect)
        except:
            return 'Не удалось изменить директорию!'
    elif request.method == 'GET':
        return render_template('storage/directory_update.html', title=db_directories.name,
                               db_directories=db_directories)


# File upload
@storage.route('/directory/<int:id>/upload', methods=['POST'])
@login_required
def upload(id):
    if request.method == 'POST':
        try:
            file = request.files['file_from_user']
            name = file.filename
            user_id = current_user.id
            all_users_directories = Directories.query.filter_by(user_id_value=user_id).all()
            print(all_users_directories)
            for direc in all_users_directories:
                test_model = UploadedFiles.query.filter_by(parent_id_value=direc.id).all()
                for model in test_model:
                    if model.name == name:
                        return 'Такой файл уже загружен. Дубликатов быть не должно.'
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads', str(id), name)
            file.save(path)
            upload_model = UploadedFiles(parent_id_value=id, name=name, download_count=0)
            db.session.add(upload_model)
            db.session.commit()
            home_redirect = '/directory/' + str(id)
            return redirect(home_redirect)
        except:
            return 'Не удалось сохранить файл! Обратитесь к администратору.'


# File delete
@storage.route('/directory/<int:id>/delete', methods=['POST'])
@login_required
def file_delete_from_directory(id):
    if request.method == 'POST':
        try:
            db_file = db.session.query(UploadedFiles).filter_by(id=id).first()
            parent_id = UploadedFiles.query.get_or_404(
                id).parent_id_value
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads', str(parent_id),
                                db_file.name)
            # delete file
            os.remove(path)
            # delete row from Data Base
            db.session.delete(db_file)
            db.session.commit()
            # return to directory
            home_redirect = '/directory/' + str(parent_id)
            return redirect(home_redirect)
        except:
            return 'Не удалось удалить файл! Обратитесь к администратору.'


# Download file
# Решить вопрос с путем сохранения файла у других пользователей!!!
@storage.route('/directory/<int:id>/download', methods=['POST'])
@login_required
def file_download(id):
    if request.method == 'POST':
        try:
            db_file = db.session.query(UploadedFiles).filter_by(id=id).first()
            parent_id = UploadedFiles.query.get_or_404(
                id).parent_id_value
            name = db_file.name
            path_from = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads', str(parent_id),
                                     name)
            # My way to download files
            path_to = os.path.join(os.path.expandvars("%userprofile%"), "Downloads", name)
            shutil.copyfile(path_from, path_to, follow_symlinks=True)
            db_file.download_count += 1
            db.session.commit()
            flash('<div class="alert alert-success">Загрузка прошла успешно</div>')
            home_redirect = '/directory/' + str(parent_id)
            return redirect(home_redirect)
        except:
            parent_id = UploadedFiles.query.get_or_404(
                id).parent_id_value
            flash('<div class="alert alert-danger">Не удалось загрузить файл! Обратитесь к администратору.</div>')
            home_redirect = '/directory/' + str(parent_id)
            return redirect(home_redirect)


# Remove file
@storage.route('/directory/<int:id>/remove', methods=['POST', 'GET'])
@login_required
def file_remove_from_directory(id):
    if request.method == 'POST':
        try:
            directory_to_move_id = request.form['directory_to_move_id']
            directory_from_move_id = UploadedFiles.query.filter_by(id=id).first()
            name = UploadedFiles.query.filter_by(id=id).first().name
            path_from = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads',
                                     str(directory_from_move_id.parent_id_value),
                                     name)
            path_to = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads',
                                   str(directory_to_move_id),
                                   name)
            # file remove
            shutil.move(path_from, path_to)
            home_redirect = '/directory/' + str(directory_from_move_id.parent_id_value)
            # change parent id
            directory_from_move_id.parent_id_value = directory_to_move_id
            db.session.commit()
            return redirect(home_redirect)

        except:
            return 'Не удалось переместить файл! Обратитесь к администратору.'
    elif request.method == 'GET':
        return render_template('storage/index.html', title='Перемещение файла')
    else:
        return 'Произошла неизвестная ошибка! Обратитесь к администратору.'

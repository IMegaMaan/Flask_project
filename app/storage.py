from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
import os
from .models import Directories, UploadedFiles
import shutil
from .forms import DirectoriesForm, FileForm


storage = Blueprint('storage', __name__)


# Home page
@storage.route('/')
def index():
    return render_template('storage/index.html', title='Домашняя страница')


# Create directory
@storage.route('/create_directory', methods=['POST', 'GET'])
@login_required
def create_directory():
    form = DirectoriesForm()
    if request.method == 'POST' and request.form['name'] != '':
        name = form.name.data
        description = form.description.data if form.description.data else ''
        #Create directory in SQL table
        #Connect to data base by user name and password
        user_session = current_user.connect_to_database()
        directory = Directories(name=name, description=description, user_id_value=current_user.id)
        user_session.add(directory)
        user_session.commit()
        #Disconnect from data base
        user_session.close()
        return redirect(url_for('storage.create_directory'))
    elif request.method == 'GET':
        return render_template('storage/create_directory.html', title='Создание директории', form=form)
    else:
        return 'Некорректное создание формы! Обратитесь к администратору!'


# Change Name and Description of Directory
@storage.route('/directory/update/<int:id>', methods=['POST', 'GET'])
@login_required
def directory_update(id):
    # Connect to data base by using user name and password
    user_session = current_user.connect_to_database()
    db_directories = user_session.query(Directories).filter_by(id=id).first()
    form = DirectoriesForm()
    if request.method == 'POST':
        # 1)распарсить request метод из json
        # new_directory = request.get_json()
        # 2) внести изменения в json
        # new_directory
        # 3) отправить измененный json



        db_directories.name = form.name.data
        db_directories.description = form.description.data
        id = db_directories.id
        user_session.commit()
        user_session.close()
        home_redirect = '/directory/' + str(id)
        return redirect(home_redirect)
    elif request.method == 'GET':
        form.name.data = db_directories.name
        form.description.data = db_directories.description
        # jsonify(post.to_json())
        return render_template('storage/directory_update.html', title=db_directories.name,
                               db_directories=db_directories, form=form)





# Directories views
@storage.route('/directories')
@login_required
def directories():
    #Connect to data base by using user name and password
    user_session = current_user.connect_to_database()
    db_directories = user_session.query(Directories).filter_by(user_id_value=current_user.id).all()
    user_session.close()
    total_directories = []
    stop = 0
    # For visual display 3 pieces in a row
    while stop < len(list(db_directories)):
        start = stop
        stop += 3
        total_directories.append(db_directories[start:stop:1])
    db_directories = total_directories
    return render_template('storage/directories.html', title='Хранилище файлов', db_directories=db_directories)


# One directory view
@storage.route('/directory/<string:id>')
@login_required
def directory(id):
    form = FileForm()
    # Connect to data base by using user name and password
    user_session = current_user.connect_to_database()
    db_all_directories = user_session.query(Directories).order_by(Directories.date).filter_by(user_id_value=current_user.id).all()
    db_directories = user_session.query(Directories).get(id)
    db_files = user_session.query(UploadedFiles).filter_by(parent_id_value=id).all()
    # Disconnect from user session
    user_session.close()
    return render_template('storage/directory.html', title=db_directories.name, db_directories=db_directories,
                           db_files=db_files, db_all_directories=db_all_directories, form=form)


# Delete the directory and all files inside
@storage.route('/directory/delete/<int:id>', methods=['POST', 'GET'])
@login_required
def directory_delete(id):
    if request.method == 'POST':
        # Connect to data base by using user name and password
        user_session = current_user.connect_to_database()
        db_directoriy = user_session.query(Directories).filter_by(id=id).first()
        children_files = user_session.query(UploadedFiles).filter_by(parent_id_value=id).all()
        # delete information with related files
        for record in children_files:
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads', record.name_to_download)
            os.remove(path)
            user_session.delete(record)
        # Delete information about parent directory
        user_session.delete(db_directoriy)
        user_session.commit()
        # Disconnect from user session
        user_session.close()
        return redirect(url_for('storage.directories'))


# File upload
@storage.route('/file/upload/<int:id>', methods=['POST'])
@login_required
def upload(id):
    form = FileForm()
    if request.method == 'POST':
        name = form.file.data.filename
        user_id = current_user.id
        # Connect to data base by using user name and password
        user_session = current_user.connect_to_database()
        all_users_directories = user_session.query(Directories).filter_by(user_id_value=user_id).all()
        # Check for duplicates
        for direc in all_users_directories:
            test_model = UploadedFiles.query.filter_by(parent_id_value=direc.id).all()
            for model in test_model:
                if model.name == name:
                    return 'Такой файл уже загружен. Дубликатов быть не должно.'
        filename = form.file.data.filename
        name_to_download = current_user.name + filename
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads', name_to_download)
        form.file.data.save(path)
        upload_model = UploadedFiles(parent_id_value=id, name=name, download_count=0, name_to_download=name_to_download)
        user_session.add(upload_model)
        user_session.commit()
        #Disconnect from data base
        user_session.close()
        home_redirect = '/directory/' + str(id)
        return redirect(home_redirect)


# File delete
# Checked test is ok
@storage.route('/file/delete/<int:id>', methods=['POST'])
@login_required
def file_delete_from_directory(id):
    if request.method == 'POST':
        # Connect to data base by using user name and password
        user_session = current_user.connect_to_database()
        db_file = user_session.query(UploadedFiles).filter_by(id=id).first()
        parent_id = db_file.parent_id_value
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads', db_file.name_to_download)
        # delete file
        os.remove(path)
        # delete row from Data Base
        user_session.delete(db_file)
        user_session.commit()
        user_session.close()
        # return to directory
        home_redirect = '/directory/' + str(parent_id)
        return redirect(home_redirect)


# Download file
# Решить вопрос с путем сохранения файла у других пользователей!!!
@storage.route('/file/download/<int:id>', methods=['POST'])
@login_required
def file_download(id):
    if request.method == 'POST':
        # Connect to data base by using user name and password
        user_session = current_user.connect_to_database()
        db_file = user_session.query(UploadedFiles).filter_by(id=id).first()
        parent_id = db_file.parent_id_value
        name_to_download = db_file.name_to_download
        path_from = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads', name_to_download)
        # My way to download files
        path_to = os.path.join(os.path.expandvars("%userprofile%"), "Downloads", db_file.name)
        shutil.copyfile(path_from, path_to, follow_symlinks=True)
        db_file.download_count += 1
        user_session.commit()
        #Disconnect from user database
        user_session.close()
        flash('<div class="alert alert-success">Загрузка прошла успешно</div>')
        home_redirect = '/directory/' + str(parent_id)
        return redirect(home_redirect)


# Remove file
@storage.route('/file/remove/<int:id>', methods=['POST', 'GET'])
@login_required
def file_remove_from_directory(id):
    if request.method == 'POST':
        directory_to_move_id = request.form['directory_to_move_id']
        # Connect to data base by using user name and password
        user_session = current_user.connect_to_database()
        directory_from_move_id = user_session.query(UploadedFiles).filter_by(id=id).first()
        home_redirect = '/directory/' + str(directory_from_move_id.parent_id_value)
        # change parent id
        directory_from_move_id.parent_id_value = directory_to_move_id
        user_session.commit()
        # Disconnect from user database
        user_session.close()
        return redirect(home_redirect)
    elif request.method == 'GET':
        return render_template('storage/index.html', title='Перемещение файла')

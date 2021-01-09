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
    response = {
        "params": {'title': 'Домашняя страница'}
    }
    return render_template('storage/index.html', response=response)


# Create directory
@storage.route('/create_directory', methods=['POST', 'GET'])
@login_required
def create_directory():
    print(request.method)
    if request.method == 'POST':
        #Work with JSON-rpc object
        response = request.get_json()
        print(response)
        name = response['params']['form']['name']
        description = response['params']['form']['description'] if response['params']['form']['description'] else ''
        #Create directory in SQL table
        #Connect to data base by user name and password
        user_session = current_user.connect_to_database()
        directory = Directories(name=name, description=description, user_id_value=current_user.id)
        user_session.add(directory)
        user_session.commit()
        directory_json = directory.to_json()
        #Disconnect from data base
        user_session.close()
        # Return JSON
        return jsonify({
            "jsonrpc": "2.0",
            "method": "create_directory",
            "params": {'directory': directory_json},
            "id": current_user.id
        })
    elif request.method == 'GET':
        form = DirectoriesForm()
        response = {
            "params": {'title': 'Создание директории', 'form': form.form_to_json()}
        }
        return render_template('storage/create_directory.html', response=response)
    else:
        return 'Некорректное создание формы! Обратитесь к администратору!'


# Change Name and Description of Directory
@storage.route('/directory/update/<int:id>', methods=['POST', 'GET'])
@login_required
def directory_update(id):
    # Connect to data base by using user name and password
    user_session = current_user.connect_to_database()
    db_directories = user_session.query(Directories).filter_by(id=id).first()
    if request.method == 'POST':
        directory = request.get_json()
        db_directories.name = directory['params']['form']['name']
        db_directories.description = directory['params']['form']['description']
        id = db_directories.id
        user_session.commit()
        db_directories_json = db_directories.to_json()
        user_session.close()
        # Return JSON
        return jsonify({
            "jsonrpc": "2.0",
            "method": "refresh_directory",
            "params": {'title': 'Создание директории', 'db_directories': db_directories_json},
            'id': id
        })
    elif request.method == 'GET':
        form = DirectoriesForm()
        form.name.data = db_directories.name
        form.description.data = db_directories.description
        response = {
            "params": {'title': db_directories.name, 'form': form.form_to_json(), 'db_directories': db_directories}
        }
        return render_template('storage/directory_update.html', response=response)


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
    response = {
        "params": {'title': 'Хранилище файлов', 'db_directories': db_directories}
    }
    return render_template('storage/directories.html', response=response)


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
    response = {
        "params": {'title': db_directories.name, 'form': form.form_to_json(), 'db_directories': db_directories,
                   'db_files': db_files, 'db_all_directories': db_all_directories}
    }
    return render_template('storage/directory.html', response=response)


# Delete the directory and all files inside
# need frontend
@storage.route('/directory/delete/<int:id>', methods=['POST'])
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
        return jsonify({
            "jsonrpc": "2.0",
            "method": "deleted_directory",
            "params": {'title': 'Хранилище файлов','home_redirect': url_for('storage.directories')},
            'id': id
        })


# File upload
@storage.route('/file/upload/<int:id>', methods=['POST'])
@login_required
def upload(id):
    if request.method == 'POST':
        response = request.get_json()
        filename = response['params']['form'].data.filename
        # name = form.file.data.filename
        user_id = current_user.id
        # Connect to data base by using user name and password
        user_session = current_user.connect_to_database()
        all_users_directories = user_session.query(Directories).filter_by(user_id_value=user_id).all()
        # Check for duplicates
        for direc in all_users_directories:
            test_model = UploadedFiles.query.filter_by(parent_id_value=direc.id).all()
            for model in test_model:
                if model.name == filename:
                    return 'Такой файл уже загружен. Дубликатов быть не должно.'
        # filename = form.file.data.filename
        name_to_download = current_user.name + filename
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads', name_to_download)
        response[1]['file'].data.save(path)
        # form.file.data.save(path)
        upload_model = UploadedFiles(parent_id_value=id, name=filename, download_count=0, name_to_download=name_to_download)
        json_object = upload_model.to_json()
        user_session.add(upload_model)
        user_session.commit()
        #Disconnect from data base
        user_session.close()
        return jsonify({
            "jsonrpc": "2.0",
            "method": "file_uploaded",
            "params": {'json_object': json_object},
            'id': id
        })


# File delete
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
        return jsonify({
            "jsonrpc": "2.0",
            "method": "file_deleted",
            "params": {'db_file': db_file},
            'id': parent_id
        })


# Download file
@storage.route('/file/download/<int:id>', methods=['POST'])
@login_required
def file_download(id):
    if request.method == 'POST':
        # Connect to data base by using user name and password
        user_session = current_user.connect_to_database()
        db_file = user_session.query(UploadedFiles).filter_by(id=id).first()
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
        return jsonify({
            "jsonrpc": "2.0",
            "method": "file_download",
            "params": {'db_file': db_file},
            'id': id
        })


# Remove file
@storage.route('/file/remove/<int:id>', methods=['POST', 'GET'])
@login_required
def file_remove_from_directory(id):
    if request.method == 'POST':
        response = request.get_json()
        directory_to_move_id = response['params']['file']['directory_to_move_id']
        # directory_to_move_id = request.form['directory_to_move_id']
        # Connect to data base by using user name and password
        user_session = current_user.connect_to_database()
        directory_from_move_id = user_session.query(UploadedFiles).filter_by(id=id).first()
        # change parent id
        directory_from_move_id.parent_id_value = directory_to_move_id
        user_session.commit()
        # Disconnect from user database
        user_session.close()
        return jsonify({
            "jsonrpc": "2.0",
            "method": "file_removed",
            "params": {'directory_from_move_id': directory_from_move_id, 'directory_to_move_id': directory_to_move_id},
            'id': id
        })
    elif request.method == 'GET':
        response = {
            "params": {'title': 'Перемещение файла'}
        }
        return render_template('storage/index.html', response=response)

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from . import db

# import sqlalchemy
# from sqlalchemy import create_engine


# model for definition directory
class Directories(db.Model):
    __tablename__ = 'directory'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=True)
    description = db.Column(db.String(400), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())
    user_id_value = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    uploaded_files = db.relationship("UploadedFiles", backref="directory")

    def __repr__(self):
        return '<Directories %r>' % self.id

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# model for definition files from users
class UploadedFiles(db.Model):
    __tablename__ = 'uploads'
    id = db.Column(db.Integer, primary_key=True)
    download_count = db.Column(db.Integer, default=0)
    name = db.Column(db.String(50), nullable=True)
    date = db.Column(db.DateTime, default=datetime.now())
    parent_id_value = db.Column(db.Integer, db.ForeignKey('directory.id'), nullable=True)

    def __repr__(self):  # в случае обращения к объекту класса, будет выдаваться объект и id
        return '<UploadedFiles %r>' % self.id

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# User model
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(50), nullable=True)
    name = db.Column(db.String(50), nullable=True, unique=True)
    directories = db.relationship("Directories", backref="user")

    '''
    #тестовые методы для работы с БД
    # добавление методов на работу с БД
    # connection method
    def connect(self, db, host='localhost', port=5432):
        """Returns a connection and a metadata object"""
        # We connect with the help of the PostgreSQL URL
        url = f'postgresql://{self.name}:{self.password}@{host}:{port}/{db}'

        # The return value of create_engine() is our connection object
        con = sqlalchemy.create_engine(url, client_encoding='utf8')

        # We then bind the connection to MetaData()
        meta = sqlalchemy.MetaData(bind=con, reflect=True)

        return con, meta

    # create table method
    def createTable(self):
        db = create_engine(self.db_string)
        db.execute("CREATE TABLE IF NOT EXISTS films (title text, director text, year text)")


    #add a new directory method
    def add_new_directory(self):
        # подключение к БД
        db_string = "postgresql+psycopg2://self.name:self.password@localhost/postgres"
        db.execute("INSERT INTO films(title, director, year) VALUES (%s,%s, %s)", title, director, year)

    #and more methods for work with files 
    '''

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User(id='%s', name='%s', password='%s')>" % (self.id, self.name, self.password)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


'''
# additional model for role setting
class Role(db.Model):
    __tablename__ = 'uploads'
    id = db.Column(db.Integer, primary_key=True)
    download_count = db.Column(db.Integer, default=0)
    name = db.Column(db.String(50), nullable=True)
    date = db.Column(db.DateTime, default=datetime.now())
    parent_id_value = db.Column(db.Integer, db.ForeignKey('directory.id'), nullable=True)

    def __repr__(self):  # в случае обращения к объекту класса, будет выдаваться объект и id
        return '<UploadedFiles %r>' % self.id

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

'''

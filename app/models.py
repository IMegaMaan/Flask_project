from flask import url_for
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime
from . import db


# model for definition directory
class Directories(db.Model):
    __tablename__ = 'directory'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=True)
    description = db.Column(db.String(400), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    user_id_value = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    uploaded_files = db.relationship("UploadedFiles", backref="directory")

    def to_json(self):
        json_directory = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'date': self.date,
            'user_id_value': self.user_id_value
        }
        return json_directory

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
    date = db.Column(db.DateTime, default=datetime.now)
    parent_id_value = db.Column(db.Integer, db.ForeignKey('directory.id'), nullable=True)
    # Additional information about full pathname of file. it may be delete by changing mechanic of usage information
    # of name
    name_to_download = db.Column(db.String(90), nullable=True, unique=True)

    def __repr__(self):
        return '<UploadedFiles %r>' % self.id

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_json(self):
        json_file = {
            'id': self.id,
            'download_count': self.download_count,
            'name': self.name,
            'date': self.date,
            'parent_id_value': self.parent_id_value,
            'name_to_download': self.name_to_download
        }
        return json_file


# User model
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(200), nullable=True)
    name = db.Column(db.String(50), nullable=True, unique=True)
    directories = db.relationship("Directories", backref="user")
    # Roles of Users. Default = 1. Just a User
    role = db.Column(db.Integer, db.ForeignKey('roles.id'), default=1)

    def __repr__(self):
        return "<User(id='%s', name='%s', password='%s')>" % (self.id, self.name, self.password)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def role_name(self):
        '''
        this metod create name of role for SQL
        :return: new_name without '@' inside
        '''
        return (''.join(self.name.split(sep='@'))).lower()

    def connect_to_database(self, database_name='flask_database'):
        '''
        Method create session of current user
        :return: user_session
        '''
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        url = "127.0.0.1:5432"
        some_engine = create_engine(
            'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=self.role_name(), pw=self.password,
                                                                  url=url,
                                                                  db=database_name))
        Session = sessionmaker(bind=some_engine)
        user_session = Session()
        return user_session

    def to_json(self):
        json_user = {
            'username': self.name,
            'role': self.role,
            'role_name': self.role_name()
        }
        return json_user




# Model for role definition
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True, unique=True)
    users = db.relationship("User", backref="roles")

    def __repr__(self):
        return '<Role %r>' % self.id

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_json(self):
        json_role = {
            'id': self.id,
            'name': self.name
        }
        return json_role

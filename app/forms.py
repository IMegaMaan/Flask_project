from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField, FileField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()],
                       render_kw={'type': "email", 'id': "inputEmail", 'class': "form-control",
                                  'placeholder': "Логин", 'required autofocus': ""})
    password = PasswordField('password', validators=[DataRequired()],
                             render_kw={'type': "password", 'id': "inputPassword", 'class': "form-control",
                                        'placeholder': "Пароль", 'required': 'True'})
    checkbox = BooleanField('Запомнить меня',
                            render_kw={'value': "remember-me", 'class': "checkbox mb-3", 'id': 'checkbox'})
    submit = SubmitField('Вход', render_kw={'class': "btn btn-lg btn-primary btn-block", 'type': "submit", 'id': "submit"})

    def form_to_json(self):
        json_login_form = {
            'name': self.name,
            'password': self.password,
            'checkbox': self.checkbox,
            'submit': self.submit
        }
        return json_login_form


class Registration(FlaskForm):
    username = StringField('username', validators=[DataRequired()],
                           render_kw={'type': "email", 'id': "inputName", 'class': "form-control",
                                      'placeholder': "Логин", 'required autofocus': ""})
    password = PasswordField('password', validators=[DataRequired()],
                             render_kw={'type': "password", 'id': "inputPassword", 'class': "form-control",
                                        'placeholder': "Пароль", 'required': 'True'})
    password_repeat = PasswordField('password_repeat', validators=[DataRequired()],
                                    render_kw={'type': "password", 'id': "inputPasswordRepeat", 'class': "form-control",
                                               'placeholder': "Повторите Пароль", 'required': 'True'})
    submit = SubmitField('Вход', render_kw={'class': "btn btn-lg btn-primary btn-block", 'type': "submit"})

    def form_to_json(self):
        json_registration_form = {
            'username': self.username,
            'password': self.password,
            'password_repeat': self.password_repeat,
            'submit': self.submit
        }
        return json_registration_form


class DirectoriesForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()],
                       render_kw={'class': "form-control", 'id': "name", "placeholder": "Имя директории"})
    description = TextAreaField('description', render_kw={'class': "form-control", 'id': "description",
                                                          'placeholder': "Описание для директории или важные заметки"})
    submit = SubmitField('Создать', render_kw={'type': "submit", 'class': "btn btn-warning", 'id': 'submit'})

    def form_to_json(self):
        json_directory_form = {
            'name': self.name,
            'description': self.description,
            'submit': self.submit
        }
        return json_directory_form


class FileForm(FlaskForm):
    file = FileField('file', render_kw={'type': "file"})
    submit = SubmitField('Загрузить', render_kw={'type': "submit", 'class': "btn btn-success"})

    def form_to_json(self):
        json_file_form = {
            'file': self.file,
            'submit': self.submit
        }
        return json_file_form

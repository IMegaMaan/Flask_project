# Flask_project
Приложение предназначено для создания директорий, загружайте и скачивайте файлы, перемещайте внутри директорий- только для зарегистрированных пользователей/ This Flask project may create directory, upload and download files into directories for registered users.
Для использвания только на локальном сервере/ Only for using upon the local machine
## 0. Перед запуском, настройте переменную/Before run app:
python

Windows:
set FLASK_APP = app

Lunix:
export FLASK_APP = app


## 1. Создание БД/Data base create

В терминале/ in console:
```
python
>>>from app import db, create_app
>>>from config import DevelopmentConfig
>>>db.create_all(app=create_app(DevelopmentConfig))
```

## 2. Настройка Пути сохранения загружаемых файлов/Setting the save path for uploaded files
storage.py, строка(row)178

Измените директорию для сохранения загружаемых файлов, если она у Вас другая/Change the path to save the file, if you have a different way of saving files
Приемлемо прямое указание пути сохранения файлов/Direct indication of the file save path is acceptable 

### Мой текущий пть для сохранения файлов/ My current path to download files
path_to = os.path.join(os.path.expandvars("%userprofile%"), "Downloads", name)

## 3. Запуск приложения через терминал/Run app through the console
`python manage.py runserver`

## 4. Использование приложения/App use
- Зарегестрируйтесь/ Signup
- Войдите в систему под учетной записью / Login to the app
- Добавляйте директории для хранения файлов- описание и название можно изменять в процессе использвания / Add directories for file storage - description and name may change during use
- Загружайте и перемещайте файлы внутри директорий пользователя. Названия файлов одного пользвателя с тем же расширением не должны повторяться / Upload and remove files inside all user directories. You can't upload file with the same name in one extension


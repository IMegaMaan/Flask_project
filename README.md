# Flask_project
This Flask project may create directory, upload and download files into directories for registered users

## 1. Создание БД/Data base create
   
- from app import db, create_app
- db.create_all(app=create_app()) 
-	При необходимости:
  If necessary:
	set FLASK_APP = app	
	
## 2. Настройка Пути сохранения загружаемых файлов/Setting the save path for uploaded files
storage.py, строка(row)178

Измените директорию для сохранения загружаемых файлов, если она у Вас другая/Change the path to save the file, if you have a different way of saving files
Приемлемо прямое указание пути сохранения файлов/Direct indication of the file save path is acceptable 

### My way to download files
path_to = os.path.join(os.path.expandvars("%userprofile%"), "Downloads", name)

## 3. Запуск приложения через терминал/Run app thru the terminal
flask run

## 4. Использвание приложения/App use
- Зарегестрируйтесь
- Войдите в систему под учетной записью
- Добавляйте директории для хранения файлов- описание и название можно изменять в процессе использвания
- Загружайте и перемещайте файлы внутри директорий пользователя. Названия файлов одного пользвателя не должны повторяться. 


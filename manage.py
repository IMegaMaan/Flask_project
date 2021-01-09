import os
from app import create_app, db
from app.models import User, Role, Directories, UploadedFiles
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from config import DevelopmentConfig

app = create_app(DevelopmentConfig)
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Directories=Directories, UploadedFiles=UploadedFiles)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    '''
        Unittest launch by command:
        python manage.py test
    '''
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)



if __name__ == '__main__':
    manager.run()

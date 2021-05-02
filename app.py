from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import Conf
from flask_babelex import Babel



app = Flask(__name__)
app.config.from_object(Conf)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
login_manager = LoginManager(app)
babel = Babel(app)
manager.add_command('db', MigrateCommand)


@babel.localeselector
def get_locale():
        # Put your logic here. Application can store locale in
        # user profile, cookie, session, etc.
        return 'ru'


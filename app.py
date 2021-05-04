from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from config import Conf
from flask_babelex import Babel

def auto_constraint_name(constraint, table):
    if constraint.name is None or constraint.name == "_unnamed_":
        return "sa_autoname_%s" % str(uuid.uuid4())[0:5]
    else:
        return constraint.name

NAMING_CONVENTION = {
    "auto_constraint_name": auto_constraint_name,
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(auto_constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
_metadata = MetaData(naming_convention=NAMING_CONVENTION)

app = Flask(__name__)
app.config.from_object(Conf)

db = SQLAlchemy(app, metadata=_metadata)
migrate = Migrate(app, db, render_as_batch=True)
manager = Manager(app)
login_manager = LoginManager(app)
babel = Babel(app)
manager.add_command('db', MigrateCommand)


@babel.localeselector
def get_locale():
    # Put your logic here. Application can store locale in
    # user profile, cookie, session, etc.
    return 'ru'

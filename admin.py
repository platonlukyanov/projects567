from app import app
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import *

admin = Admin(app, template_mode='bootstrap4')
admin.add_view(ModelView(UserType, db.session))
admin.add_view(ModelView(Project, db.session))
admin.add_view(ModelView(Subject, db.session))



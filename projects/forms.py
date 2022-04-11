from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.fields import FileField, MultipleFileField
from wtforms.validators import InputRequired, URL, Optional
from form_widgets import *
from models import *
from app import app


class ProjectUploadForm(FlaskForm):
    name = StringField("Введите имя проекта...", widget=VerifyText(), validators=[InputRequired()])
    subject = SelectField("Предмет:", choices=[(s.id, s.name) for s in Subject.query.order_by('name')], coerce=int,
                          widget=VerifySelect(), validators=[InputRequired()])
    desc = StringField("Описание проекта: ", widget=VerifyTextArea(), validators=[Optional()])
    project_image = FileField("Заглавное изображение вашего проекта", widget=VerifyFile(), validators=[Optional()],
                              render_kw={'accept': "." + ", .".join(app.config["IMAGE_ALLOWED_EXTENSIONS"])})
    project_files = MultipleFileField("Файлы: ", widget=VerifyFile(multiple=True),
                                      render_kw={'webkitdirectory': True, 'directory': True})

    site_url = StringField("Сайт: ", widget=VerifyURL(), validators=[URL(message="Неккоректный URL адрес"), Optional()])

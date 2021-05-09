from app import app
from flask import request, redirect, url_for
from flask_login import current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from models import *


class AdminMixin:
    def is_accessible(self):
        return current_user.admin_access

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect('/')
        else:
            return redirect(url_for('login') + "?next=" + request.url)


class AdminView(AdminMixin, ModelView, ):
    pass


class HomeAdminView(AdminMixin, AdminIndexView, ):
    pass


class BaseModelView(ModelView):

    def on_model_change(self, form, model, is_created):
        try:
            model.generate_slug()
        except:
            pass
        return super(BaseModelView, self).on_model_change(form, model, is_created)


class ProjectAdminView(AdminMixin, ModelView):
    can_create = False
    form_columns = ["name", "desc", "users", "active", "is_best"]
    column_exclude_list = ['path_to_index', 'path_to_tphoto', 'slug', 'site_url']
    column_searchable_list = ['name', "desc"]
    column_filters = ['created', 'active', 'type', 'has_photo']
    column_editable_list = ["active", "is_best"]
    can_export = True
    column_labels = dict(name="Название", desc="Описание", created="Дата публикации", type="Тип", subject="Предмет",
                         has_photo="Наличие фотографии", users="Пользователи", active="Доступен", is_best="Отображен на главной")
    column_default_sort = ("created", True)
    column_choices = {
        'type': [
            (0, 'Без файлов'),
            (1, 'С файлами'),
            (2, 'Сайт'),
            (None, '')
        ]
    }
    column_formatters = dict(subject=lambda v, c, m, p: m.subject.name)


class SubjectAdminView(AdminMixin, BaseModelView):
    form_columns = ["name", "projects"]
    column_exclude_list = ['slug']
    column_editable_list = ['name']
    can_export = True
    column_labels = dict(name="Имя", projects="Проекты")
    create_modal = True


class UserTypeAdminView(AdminMixin, BaseModelView):
    column_exclude_list = ['slug']
    column_editable_list = ['name']
    column_labels = dict(name="Имя")
    create_modal = True
    form_excluded_columns = ["users", "slug"]


class UserAdminView(AdminMixin, BaseModelView):
    can_export = True
    can_create = False
    column_editable_list = ['usertype', 'admin_access']
    column_exclude_list = ['password']
    form_excluded_columns = ["password", "projects_suggests", "projects"]
    column_formatters = dict(usertype=lambda v, c, m, p: m.usertype.name)
    column_labels = dict(first_name="Имя", last_name="Фамилия", email="Электронная почта", usertype="Тип пользователя",
                         admin_access="Доступ к панели администрации")


admin = Admin(app, 'Проекты 567', index_view=HomeAdminView(name="Главная"), url="/", template_mode='bootstrap4')
admin.add_view(SubjectAdminView(Subject, db.session, name="Предметы"))
admin.add_view(UserAdminView(User, db.session, name="Пользователи"))
admin.add_view(ProjectAdminView(Project, db.session, name="Проекты"))
admin.add_view(UserTypeAdminView(UserType, db.session, name="Типы пользователя"))

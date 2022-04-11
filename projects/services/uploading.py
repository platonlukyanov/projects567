from models import *
from utils import make_all_dirs_of_path, allowed_image
import os
import shutil
from werkzeug.utils import secure_filename
import time
from flask_login import current_user
from app import db, app


def parse_upload_form(form, request):
    """Возвращает данные формы загрузки проекта в виде словаря"""
    return {
        "name": form.name.data,
        "description": form.desc.data,
        "subject": Subject.query.get(int(form.subject.data)),
        "project_files": form.project_files.data,
        "project_image": form.project_image.data,
        "site_url": form.site_url.data,
        "project_type": int(request.form.get("type")),
    }


def read_path_to_index(upload_folder, file, project_object):
    """Определяет путь к стартовой странице и записывает его в аттрибут переданного объекта"""
    filename = project_object.slug + "/" + file.filename
    if file.filename.split('/')[-1] == "index.html":
        project_object.path_to_index = upload_folder.replace("static/", "") + filename
    return project_object


def save_project_files(project_files, project_object, upload_folder):
    """Сохраняет все файлы из project_files в upload_folder"""
    for file in project_files:
        filename = project_object.slug + "/" + file.filename
        print(os.path.join(upload_folder, filename))
        make_all_dirs_of_path(filename, upload_folder)
        try:
            file.save(os.path.join(upload_folder, filename))
        except:
            print(filename)
        if project_object.type == 2:
            project_object = read_path_to_index(upload_folder, file, project_object)


def set_project_image(project_image, project_object):
    """Сохраняет титульное изображение и определяет путь к титульному изображению проекта и записывает его в аттрибут переданного объекта"""
    if project_image and project_image.filename != '' and allowed_image(project_image):
        project_object = save_project_image(project_image, project_object,
                                            upload_form=app.config['PROJECT_TITLE_IMAGE_FOLDER'])
    else:
        project_object.path_to_tphoto = 'images/nofoto.png'
    return project_object


def save_project_image(project_image, project_object, upload_form):
    """Сохраняет титульную картинку проекта в директории"""
    filename = secure_filename(project_image.filename)
    path_to_tphoto = app.config['PROJECT_TITLE_IMAGE_FOLDER'] + "/" + "_" + str(time.time()) + "." + \
                     filename.split(".")[-1]
    make_all_dirs_of_path(path_to_tphoto)
    project_image.save(path_to_tphoto)
    project_object.path_to_tphoto = "/".join(path_to_tphoto.split("/")[1:])
    project_object.has_photo = True
    return project_object


def create_new_project(name, description, subject, project_image, project_type, project_files, site_url):
    """Создает проект(в том числе сохраняя нужные файлы)"""
    obj = Project(name=name, desc=description, subject_id=subject.id, type=project_type)
    upload_folder = app.config["UPLOAD_FOLDER"]
    if len(project_files) > 1 and project_type != 0:
        save_project_files(project_files, obj, upload_folder)
    obj = set_project_image(project_image, obj)
    obj.site_url = site_url
    obj.users.append(current_user)
    if project_type != 0:
        if (obj.path_to_index and project_type == 2) or project_type == 1:
            shutil.make_archive(f'static/archives/{obj.slug}', 'zip', os.path.join(upload_folder, obj.slug))
    ss = db.session
    ss.add(obj)
    ss.commit()
    return obj

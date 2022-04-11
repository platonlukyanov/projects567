import os
import re
from app import app


def allowed_image(imagefile):
    ext = imagefile.filename.split(".")[-1]
    return ext in app.config["IMAGE_ALLOWED_EXTENSIONS"]


def make_all_dirs_of_path(route, pre_dir=""):
    """Создает все директории на пути к файлу"""
    directories = route.split('/')[:-1]
    last_dirs = [pre_dir]
    for directory in directories:
        last_dirs.append(directory)
        path = "/".join(last_dirs)
        if not os.path.isdir(path):
            os.mkdir(path)


def replace_href(obj):
    return '''href="{{ url_for('static', filename=%s) }}"''' % re.search('".*"', obj.group(0)).group(0).replace(
        '''""''', '''"''')

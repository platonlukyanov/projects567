import os
import re

def make_all_dirs_of_path(route, pre_dir=""):
    directories = route.split('/')[:-1]
    last_dirs = [pre_dir]
    for directory in directories:
        last_dirs.append(directory)
        path = "/".join(last_dirs)
        if not os.path.isdir(path):
            os.mkdir(path)


def replace_href(obj):
    return '''href="{{ url_for('static', filename=%s) }}"''' % re.search('".*"', obj.group(0)).group(0).replace('''""''', '''"''')

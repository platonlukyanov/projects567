from flask import render_template, request, url_for, redirect, flash
import os

from werkzeug.utils import secure_filename
import time
from models import *
from app import db, app
from utils import make_all_dirs_of_path, allowed_image
from flask_login import login_required, current_user



@app.route('/')
def index():

    return render_template('index.html')



@app.route('/upload-project', methods=["POST", "GET"])
@login_required
def upload_project():
    if request.method == "POST":
        name = request.form.get("name")
        desc = request.form.get("desc")
        subject = Subject.query.filter(Subject.slug == request.form.get("subject")).first()
        proj_files = request.files.getlist("file[]")
        proj_image = request.files.get("title-image")
        path_to_index = ""
        path_to_tphoto = ""
        if len(proj_files) > 1:
            path_to_index = None

            for file in proj_files:
                make_all_dirs_of_path(file.filename, app.config["UPLOAD_FOLDER"])
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
                if file.filename.split('/')[-1] == "index.html":
                    path_to_index = "uploads/" + file.filename

        try:
            has_file = not proj_image.filename == ''
        except:
            has_file = False
        if proj_image and has_file:
            if allowed_image(proj_image):
                filename = secure_filename(proj_image.filename)
                path_to_tphoto = app.config['PROJECT_TITLE_IMAGE_FOLDER'] + "/" + "_" + str(
                    time.time())
                make_all_dirs_of_path(path_to_tphoto)
                proj_image.save(path_to_tphoto)
                path_to_tphoto = "/".join(path_to_tphoto.split("/")[1:])
        else:
            path_to_tphoto = 'images/nofoto.png'
        print(path_to_tphoto)
        obj = Project(name=name, desc=desc, subject_id=subject.id, user_id=current_user.id)
        if path_to_index:
            obj.path_to_index = path_to_index
        if path_to_tphoto:
            obj.path_to_tphoto = path_to_tphoto

        ss = db.session
        ss.add(obj)
        ss.commit()

    all_subjects = Subject.query.all()

    return render_template('upload.html', subjects=all_subjects)


@app.route('/sites/<slug>')
def render_site(slug):
    proj = Project.query.filter(Project.slug == slug).first()

    return redirect(url_for('static', filename=proj.path_to_index))

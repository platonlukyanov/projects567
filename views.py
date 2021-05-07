from flask import render_template, request, url_for, redirect, flash, send_file
import os
import shutil
from werkzeug.utils import secure_filename
import time
from models import *
from app import db, app
from utils import make_all_dirs_of_path, allowed_image
from flask_login import login_required, current_user


@app.route('/')
def index():
    all_subjects = Subject.query.all()
    return render_template('index.html', subjects=all_subjects)


@app.route('/upload-project', methods=["POST", "GET"])
@login_required
def upload_project():
    if request.method == "POST":
        name = request.form.get("name")
        desc = request.form.get("desc")
        subject = Subject.query.filter(Subject.slug == request.form.get("subject")).first()
        proj_files = request.files.getlist("file[]")
        proj_image = request.files.get("title-image")
        site_url = request.form.get("site_url")
        path_to_index = ""
        path_to_tphoto = ""
        has_photo = False
        obj = Project(name=name, desc=desc, subject_id=subject.id)
        upload_folder = app.config["UPLOAD_FOLDER"]
        if len(proj_files) > 1:
            path_to_index = None

            for file in proj_files:
                filename = obj.slug + "/" + file.filename

                make_all_dirs_of_path(filename, upload_folder)
                file.save(os.path.join(upload_folder, filename))
                if file.filename.split('/')[-1] == "index.html":
                    path_to_index = upload_folder.replace("static/", "") + filename

        try:
            has_file = proj_image.filename != ''
        except:
            has_file = False
        if proj_image and has_file:
            if allowed_image(proj_image):
                filename = secure_filename(proj_image.filename)
                path_to_tphoto = app.config['PROJECT_TITLE_IMAGE_FOLDER'] + "/" + "_" + str(time.time()) + "." + \
                                 filename.split(".")[-1]
                make_all_dirs_of_path(path_to_tphoto)
                proj_image.save(path_to_tphoto)
                path_to_tphoto = "/".join(path_to_tphoto.split("/")[1:])
                has_photo = True
        else:
            path_to_tphoto = 'images/nofoto.png'

        obj.has_photo = has_photo
        obj.site_url = site_url
        obj.users.append(current_user)
        if path_to_index:
            obj.path_to_index = path_to_index
            shutil.make_archive(f'static/archives/{obj.slug}', 'zip', os.path.join(upload_folder, obj.slug))
        if path_to_tphoto:
            obj.path_to_tphoto = path_to_tphoto

        ss = db.session
        ss.add(obj)
        ss.commit()
        return redirect(url_for('projects.project_detail', slug=obj.slug))
    all_subjects = Subject.query.all()

    return render_template('upload.html', subjects=all_subjects)


@app.route('/sites/<slug>')
def render_site(slug):
    proj = Project.query.filter(Project.slug == slug).first()

    return redirect(url_for('static', filename=proj.path_to_index))


@app.route('/downloads/projects/<slug>')
def download_project_zip(slug):
    return send_file(f'static/archives/{slug}.zip', as_attachment=True)


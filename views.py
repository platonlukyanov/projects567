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
    best_projects = Project.query.filter(Project.is_best).all()
    return render_template('index.html', subjects=all_subjects, best_projects=best_projects)


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
        project_type = int(request.form.get("type"))
        path_to_index = ""
        path_to_tphoto = ""
        has_photo = False
        obj = Project(name=name, desc=desc, subject_id=subject.id, type=project_type)
        upload_folder = app.config["UPLOAD_FOLDER"]
        if len(proj_files) > 1 and project_type != 0:
            path_to_index = None

            for file in proj_files:
                filename = obj.slug + "/" + file.filename
                print(os.path.join(upload_folder, filename))
                make_all_dirs_of_path(filename, upload_folder)
                try:
                    file.save(os.path.join(upload_folder, filename))
                except:
                    print(filename)
                if project_type == 2:
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
        if project_type != 0:
            obj.path_to_index = path_to_index
            if (obj.path_to_index and project_type == 2) or project_type == 1:
                shutil.make_archive(f'static/archives/{obj.slug}', 'zip', os.path.join(upload_folder, obj.slug))
        if path_to_tphoto:
            obj.path_to_tphoto = path_to_tphoto

        ss = db.session
        ss.add(obj)
        ss.commit()
        return render_template("after_upload.html", project=obj)
    all_subjects = Subject.query.all()

    return render_template('upload.html', subjects=all_subjects)


@app.route('/sites/<slug>')
def render_site(slug):
    proj = Project.query.filter(Project.slug == slug).first()

    return redirect(url_for('static', filename=proj.path_to_index))


@app.route('/downloads/projects/<slug>')
def download_project_zip(slug):
    return send_file(f'static/archives/{slug}.zip', as_attachment=True)


@app.route('/profile')
def user_profile():
    suggests = ProjectSuggest.query.filter(ProjectSuggest.status == 1).all()
    cur_users_projects_ids = list(map(lambda x: x.id, current_user.projects))
    suggests = [suggest for suggest in suggests if suggest.project_id in cur_users_projects_ids]
    return render_template('profile.html', suggests=suggests)

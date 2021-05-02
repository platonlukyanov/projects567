from flask import render_template, request, url_for, redirect
import os
from models import *
from app import db, app
from utils import make_all_dirs_of_path
from flask_login import login_required


@app.route('/')
def index():
    return render_template('index.html')

@login_required
@app.route('/upload-project', methods=["POST", "GET"])
def upload_project():
    print("upload")
    if request.method == "POST":
        name = request.form.get("name")
        desc = request.form.get("desc")
        subject = Subject.query.filter(Subject.slug == request.form.get("subject")).first()
        proj_files = request.files.getlist("file[]")

        path_to_index = ""

        if len(proj_files) > 1:
            path_to_index = None

            for file in proj_files:
                make_all_dirs_of_path(file.filename, app.config["UPLOAD_FOLDER"])
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
                if file.filename.split('/')[-1] == "index.html":
                    path_to_index = "uploads/" + file.filename

        obj = Project(name=name, desc=desc, subject=subject.id)
        if path_to_index:
            obj.path_to_index = path_to_index
        ss = db.session
        ss.add(obj)
        ss.commit()

    all_subjects = Subject.query.all()

    return render_template('upload.html', subjects=all_subjects)


@app.route('/sites/<slug>')
def render_site(slug):
    proj = Project.query.filter(Project.slug == slug).first()

    return redirect(url_for('static', filename=proj.path_to_index))

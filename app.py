import os
from datetime import datetime

from flask import Flask, render_template, request, url_for, redirect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from slugify import slugify

from config import Conf
from utils import make_all_dirs_of_path

app = Flask(__name__)
app.config.from_object(Conf)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String, unique=True, nullable=False)
    desc = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now)
    subject = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    path_to_index = db.Column(db.String(255))

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        self.slug = slugify(self.name)

    def __repr__(self):
        return f'<Project id: {self.id}, name: "{self.name}">'


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String, unique=True)
    projects = db.relationship('Project', lazy=True)

    def __init__(self, *args, **kwargs):
        super(Subject, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        self.slug = slugify(self.name)

    def __repr__(self):
        return f'<Subject id: {self.id}, name: "{self.name}">'


# VIEWS
@app.route('/upload-project', methods=["POST", "GET"])
def upload_project():
    if request.method == "POST":
        name = request.form.get("name")
        desc = request.form.get("desc")
        subject = Subject.query.filter(Subject.slug == request.form.get("subject")).first()
        proj = request.files.getlist("file[]")
        path_to_index = None
        paths = []
        for file in proj:
            make_all_dirs_of_path(file.filename, app.config["UPLOAD_FOLDER"])
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
            if file.filename.split('/')[-1] == "index.html":
                path_to_index = "uploads/" + file.filename
            paths.append(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
        #     if not file.filename.endswith(".html"):
        #         make_all_dirs_of_path(file.filename, app.config["CSS_UPLOAD_FOLDER"])
        #         file.save(os.path.join(app.config["CSS_UPLOAD_FOLDER"], file.filename))
        #         continue
        #
        #     last_dir = app.config.get("HTML_UPLOAD_FOLDER")
        #     make_all_dirs_of_path(file.filename, last_dir)
        #     if file.filename.split('/')[-1] == "index.html":
        #         path_to_index = "uploads/" + file.filename
        #     file.save(os.path.join(app.config["HTML_UPLOAD_FOLDER"], file.filename))
        #     paths.append(os.path.join(app.config["HTML_UPLOAD_FOLDER"], file.filename))
        #
        for path in paths:

            try:
                fr = open(path, "r", encoding="utf-8")
                content = fr.read()
                fr.close()
                f = open(path, "w", encoding="utf-8")
                # m = re.compile(r'''href="((?!").)*"''')
                # content = m.sub(replace_href, content)
                f.write(content)
                f.close()
            except Exception:
                pass

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


if __name__ == '__main__':
    app.run()

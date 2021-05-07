from flask_login import UserMixin
from app import db, login_manager
from datetime import datetime
from slugify import slugify

projects_users = db.Table('projects_users',
                          db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True),
                          db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
                          )


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.Text)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    path_to_index = db.Column(db.String(255))
    site_url = db.Column(db.String(255))
    path_to_tphoto = db.Column(db.String(255))
    has_photo = db.Column(db.Boolean, default=False)
    suggests = db.relationship('ProjectSuggest', lazy=True, backref="project")
    created = db.Column(db.DateTime, default=datetime.now)
    slug = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        slug = slugify(self.name).lower()
        if not Project.query.filter(Project.slug == slug).first():
            print(Project.query.filter(Project.slug == slug).first())
            print(bool(Project.query.filter(Project.slug == slug).first()))
            self.slug = slug
        else:
            c = 0
            while True:
                new_slug = slug + str(c)
                if not Project.query.filter(Project.slug == new_slug).first():
                    self.slug = new_slug
                    break
                c += 1

    def __repr__(self):
        return f'<Project id: {self.id}, name: "{self.name}">'


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String, unique=True)
    projects = db.relationship('Project', lazy=True, backref="subject")

    def __init__(self, *args, **kwargs):
        super(Subject, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        slug = slugify(self.name).lower()
        if not Subject.query.filter(Subject.slug == slug).first():

            self.slug = slug
        else:
            c = 0
            while True:
                new_slug = slug + str(c)
                if not Subject.query.filter(Subject.slug == new_slug).first():
                    self.slug = new_slug
                    break
                c += 1

    def __repr__(self):
        return f'<Subject id: {self.id}, name: "{self.name}">'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    password = db.Column(db.String(100), nullable=False)
    usertype_id = db.Column(db.Integer, db.ForeignKey('user_type.id'),
                            nullable=False)

    projects = db.relationship('Project', secondary=projects_users, lazy='subquery',
                               backref=db.backref('users', lazy=True))
    projects_suggests = db.relationship('ProjectSuggest', lazy=True, backref="sender")

    def __repr__(self):
        return f'<User id: {self.id}, name: "{self.first_name} {self.last_name}">'


class UserType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    users = db.relationship('User', backref='usertype', lazy=True)
    slug = db.Column(db.String, unique=True)

    def __repr__(self):
        return f'<UserType id: {self.id}, name: "{self.name}">'


class ProjectSuggest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    sent = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.Integer, default=1, nullable=False) # Three cases: 0 - canceled, 1 - active, 2 - accepted

    def __repr__(self):
        return f'<ProjectSuggest id: {self.id}, msg: "{self.message}">'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

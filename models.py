from flask_login import UserMixin
from app import db, login_manager
from datetime import datetime
from slugify import slugify


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String, unique=True, nullable=False)

    desc = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    path_to_index = db.Column(db.String(255))
    path_to_tphoto = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
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
    projects = db.relationship('Project', lazy=True, backref="subject")

    def __init__(self, *args, **kwargs):
        super(Subject, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        self.slug = slugify(self.name)

    def __repr__(self):
        return f'<Subject id: {self.id}, name: "{self.name}">'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    password = db.Column(db.String(100), nullable=False)
    usertype_id = db.Column(db.Integer, db.ForeignKey('user_type.id'),
                            nullable=False, default=1)
    projects = db.relationship('Project', lazy=True, backref="user")


class UserType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    users = db.relationship('User', backref='usertype', lazy=True)
    slug = db.Column(db.String, unique=True)

    def __init__(self, *args, **kwargs):
        super(UserType, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        self.slug = slugify(self.name)

    def __repr__(self):
        return f'<UserType id: {self.id}, name: "{self.name}">'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

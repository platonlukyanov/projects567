from flask import Blueprint, render_template, request
from models import *

projects = Blueprint('projects', __name__, template_folder='templates')


@projects.route('/')
def all_projects():
    subject_slug = request.args.get('subject', '')
    year = request.args.get('year', 0)
    print(year)
    all_subjects = Subject.query.all()
    projects = Project.query.all()
    years = list(set([i.created.year for i in projects]))


    if subject_slug:
        subject = Subject.query.filter(Subject.slug == subject_slug).first()
        projects = Project.query.filter(Project.subject_id == subject.id).all()
        name_of_subject = subject.name
    else:
        subject = object()
        name_of_subject = "Все проекты"
    projects = [i for i in projects if i.created.year == int(year) or year == 0]
    return render_template('projects/index.html', projects=projects, subject=subject, name_of_subject=name_of_subject,
                           all_subjects=all_subjects, years=years, year=year)


@projects.route('/<slug>')
def project_detail(slug):
    project = Project.query.filter(Project.slug == slug).first()

    return render_template('projects/project_detail.html', project=project)

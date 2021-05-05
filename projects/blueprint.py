from flask import Blueprint, render_template, request
from models import *
from flask_paginate import Pagination, get_page_args

projects = Blueprint('projects', __name__, template_folder='templates')


@projects.route('/')
def all_projects():
    subject_slug = request.args.get('subject', '')
    year = request.args.get('year', 0)
    print(year)
    all_subjects = Subject.query.all()
    projects = Project.query.all()
    years = sorted(list(set([i.created.year for i in projects])))[::-1]
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    if subject_slug:
        subject = Subject.query.filter(Subject.slug == subject_slug).first()
        projects = Project.query.filter(Project.subject_id == subject.id).all()
        name_of_subject = subject.name
    else:
        subject = object()
        name_of_subject = "Все проекты"
    projects = [i for i in projects if i.created.year == int(year) or year == 0]
    total_len = len(projects)
    pagination_projects = projects[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=total_len,
                            css_framework='bootstrap4')
    return render_template('projects/index.html', projects=pagination_projects, subject=subject, name_of_subject=name_of_subject,
                           all_subjects=all_subjects, years=years, year=year,
                           page=page,
                           per_page=per_page,
                           pagination=pagination)


@projects.route('/<slug>')
def project_detail(slug):
    project = Project.query.filter(Project.slug == slug).first()

    return render_template('projects/project_detail.html', project=project)

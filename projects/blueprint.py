from flask import Blueprint, render_template, request, url_for, redirect, flash, send_file
from flask_paginate import Pagination, get_page_args
from models import *
from flask_login import login_required
from projects.services.uploading import create_new_project, parse_upload_form
from projects.forms import ProjectUploadForm

projects = Blueprint('projects', __name__, template_folder='templates')


@projects.route('/')
def all_projects():
    subject_slug = request.args.get('subject', '')
    year = request.args.get('year', 0)
    q = request.args.get('q')
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    projects = Project.query.filter(Project.active).order_by(Project.created.desc()).all()
    all_subjects = Subject.query.all()
    years = sorted(list(set([i.created.year for i in projects])))[::-1]
    if q:
        projects = Project.query.filter(
            (Project.name.contains(q) | Project.desc.contains(q)) & Project.active).all()
        name_of_subject = "Результаты поиска: " + f'"{q}"'
    else:
        if subject_slug:
            subject = Subject.query.filter(Subject.slug == subject_slug).first()
            projects = Project.query.filter((Project.subject_id == subject.id) & Project.active).order_by(
                Project.created.desc()).all()
            name_of_subject = subject.name
        else:
            name_of_subject = "Все проекты"
        projects = [i for i in projects if i.created.year == int(year) or year == 0]
    total_len = len(projects)
    pagination_projects = projects[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=total_len,
                            css_framework='bootstrap4', search=bool(q))
    return render_template('projects/index.html', projects=pagination_projects,
                           name_of_subject=name_of_subject,
                           subjects=all_subjects, years=years, year=year,
                           page=page,
                           per_page=per_page,
                           pagination=pagination)


@projects.route('/upload', methods=["POST", "GET"])
@login_required
def upload_project():
    form = ProjectUploadForm()
    if form.validate_on_submit():
        form_data = parse_upload_form(form, request)
        project = create_new_project(**form_data)
        return render_template("projects/after_upload.html", project=project)
    all_subjects = Subject.query.all()
    print(form.errors)
    return render_template('projects/upload.html', subjects=all_subjects, form=form)


@projects.route('/render/<slug>')
def render_site(slug):
    proj = Project.query.filter(Project.slug == slug).first()
    return redirect(url_for('static', filename=proj.path_to_index))


@projects.route('/download/<slug>')
def download_project_zip(slug):
    return send_file(f'static/archives/{slug}.zip', as_attachment=True)


@projects.route('/<slug>')
def project_detail(slug):
    project = Project.query.filter((Project.slug == slug) & Project.active).first()
    all_subjects = Subject.query.all()
    return render_template('projects/project_detail.html', project=project, subjects=all_subjects)

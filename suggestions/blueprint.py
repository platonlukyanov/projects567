from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required, current_user
from models import *

suggestions = Blueprint('suggestions', __name__, template_folder='templates')


@suggestions.route('/create/<int:sender_id>/<int:project_id>', methods=["POST"])
def create(project_id, sender_id):
    msg = request.form.get("text")
    suggest = ProjectSuggest(message=msg, sender_id=sender_id, project_id=project_id)
    db.session.add(suggest)
    db.session.commit()
    return redirect(url_for('projects.all_projects'))


@suggestions.route('/')
@login_required
def project_suggestions():
    suggests = ProjectSuggest.query.filter(ProjectSuggest.status == 1).all()
    cur_users_projects_ids = list(map(lambda x: x.id, current_user.projects))
    suggests = [suggest for suggest in suggests if suggest.project_id in cur_users_projects_ids]
    return render_template('suggestions/index.html', suggests=suggests)


@suggestions.route('/cancel/<int:id_>')
def cancel_suggest(id_):
    suggest = ProjectSuggest.query.get(id_)
    suggest.status = 0
    db.session.commit()
    return redirect(url_for('suggestions.project_suggestions'))


@suggestions.route('/accept/<int:id_>')
def accept_suggest(id_):
    suggest = ProjectSuggest.query.get(id_)
    suggest.project.users.append(suggest.sender)
    suggest.status = 2
    db.session.commit()
    return redirect(url_for('suggestions.project_suggestions'))



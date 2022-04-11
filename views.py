from flask import render_template, url_for, redirect
from models import *
from app import app
from flask_login import current_user


@app.route('/')
def index():
    print("index")
    return redirect(url_for('projects.all_projects'))



@app.route('/profile')
def user_profile():
    suggests = ProjectSuggest.query.filter(ProjectSuggest.status == 1).all()
    cur_users_projects_ids = list(map(lambda x: x.id, current_user.projects))
    suggests = [suggest for suggest in suggests if suggest.project_id in cur_users_projects_ids]
    return render_template('profile.html', suggests=suggests)

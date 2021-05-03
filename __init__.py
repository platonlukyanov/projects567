from app import app
from projects.blueprint import projects
import views
import auth
import admin

app.register_blueprint(projects, url_prefix="/projects")


if __name__ == "__main__":
    app.run()

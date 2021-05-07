from app import app
from projects.blueprint import projects
from suggestions.blueprint import suggestions
import views
import auth
import admin

app.register_blueprint(projects, url_prefix="/projects")
app.register_blueprint(suggestions, url_prefix="/suggestions")

if __name__ == "__main__":
    app.run()

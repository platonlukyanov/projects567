from app import app
from projects.blueprint import projects
from suggestions.blueprint import suggestions
from accounts.blueprint import accounts
import views
import admin

app.register_blueprint(projects, url_prefix="/projects")
app.register_blueprint(suggestions, url_prefix="/suggestions")
app.register_blueprint(accounts, url_prefix="/accounts")


import logging
file_handler = logging.FileHandler("log.log")
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

if __name__ == "__main__":
    app.run()

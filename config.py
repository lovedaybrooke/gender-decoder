import os

basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ.get("SECRET_KEY")
default_database_uri = f'sqlite:///{os.path.join(basedir, "app/app.sqlite3")}'
DATABASE_URI = os.environ.get("DATABASE_URL", default=default_database_uri)


SQLALCHEMY_DATABASE_URI = DATABASE_URI
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, "db_repository")
SQLALCHEMY_TRACK_MODIFICATIONS = True

DEBUG = os.environ.get("DEBUG", False)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config["DATABASE_URL"])
    rv.row_factory = sqlite3.Row
    return rv

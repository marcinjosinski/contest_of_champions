import sys
import os

from flask_migrate import upgrade
from app import create_app
from app.models import Hero, Group, Fight

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = create_app()


@app.cli.command()
def deploy():
    with app.app_context():
        upgrade()
        Group.establish_enemies()

import pytest
from flask_migrate import upgrade

from app import create_app, db
from app.models import Hero, Group, GroupType


@pytest.fixture(scope='session')
def test_client():
    flask_app = create_app()

    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


@pytest.fixture(scope='session')
def init_database():
    # applies all alembic migrations
    upgrade()
    Group.establish_enemies()

    yield db

    db.drop_all()


@pytest.fixture(scope='module')
def new_hero():
    hero = Hero()
    hero.name = 'test_user'
    hero.set_password('password')
    hero.set_public_id()
    hero.health = 100
    hero.is_participant = True
    hero.group_id = GroupType.HUMAN

    return hero
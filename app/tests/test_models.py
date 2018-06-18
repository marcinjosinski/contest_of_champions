from app.models import GroupType


def test_new_hero(new_hero):
    """
    GIVEN a Hero model
    WHEN a new Hero is created
    THEN check name, hash_password, group_id, health, permissions, is_participant
    """
    assert new_hero.name == 'test_user'
    assert new_hero.password_hash != 'password'
    assert new_hero.check_password('password')
    assert new_hero.check_public_id()
    assert new_hero.health == 100
    assert new_hero.group_id == GroupType.HUMAN
    assert new_hero.is_participant


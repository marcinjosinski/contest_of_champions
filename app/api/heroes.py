from . import api, errors, decorators
from flask import request, jsonify, url_for
from app.models import Hero
from app import db


###########################
# REMEMBER TO ADD PROPER DATA VALIDATION / cerberus
###########################

@api.route('/heroes/<public_id>', methods=['PATCH'])
@decorators.token_required
@decorators.grandmaster_required
def kill_hero(current_hero, public_id):
    hero = Hero.query.filter_by(public_id=public_id).first()

    if not hero:
        return errors.bad_request('No hero found')

    hero.is_participant = False
    hero.health = 0
    db.session.add(hero)
    db.session.commit()

    return jsonify({}), 204


@api.route('/heroes/<public_id>', methods=['DELETE'])
@decorators.token_required
@decorators.grandmaster_required
def delete_hero(current_hero, public_id):

    hero = Hero.query.filter_by(public_id=public_id).first()

    if hero:
        db.session.delete(hero)
        db.session.commit()

    return jsonify({}), 204


@api.route('/heroes/<public_id>', methods=['GET'])
@decorators.token_required
@decorators.grandmaster_required
def get_hero(current_hero, public_id):

    hero = Hero.query.filter_by(public_id=public_id).first()

    if not hero:
        return errors.bad_request('No hero found')

    return jsonify(hero.to_dict())


@api.route('/heroes', methods=['GET'])
@decorators.token_required
@decorators.grandmaster_required
def get_all_heroes(current_hero):
    heroes = Hero.query.all()

    output = []

    for hero in heroes:
        output.append(hero.to_dict())

    return jsonify(output)


@api.route('/heroes', methods=['POST'])
@decorators.token_required
@decorators.grandmaster_required
def create_hero(current_hero):
    data = request.get_json() or {}

    if 'name' not in data or 'password' not in data or 'group_id' not in data:
        return errors.bad_request('please remember to include name, password and group')
    if Hero.query.filter_by(name=data['name']).first():
        return errors.bad_request('This name already exists')
    hero = Hero()
    hero.from_dict(data)
    db.session.add(hero)
    db.session.commit()
    response = jsonify(hero.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_hero', public_id=hero.public_id)
    return response


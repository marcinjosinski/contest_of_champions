from . import api, errors
from flask import request, jsonify, url_for
from app.models import Hero
from app import db


@api.route('/ranking')
def ranking():
    return 'Works'

###########################
# REMEMBER TO ADD PROPER DATA VALIDATION / cerberus
###########################


@api.route('/hero/<public_id>', methods=['GET'])
def get_hero(public_id):
    hero = Hero.query.filter_by(public_id=public_id).first()

    if not hero:
        return errors.bad_request('No hero found')
    return jsonify(hero.to_dict())


@api.route('/heroes', methods=['GET'])
def get_all_heroes():
    heroes = Hero.query.all()

    output = []

    for hero in heroes:
        output.append(hero.to_dict())

    return jsonify(output)


@api.route('/heroes', methods=['POST'])
def create_hero():
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
    # response.headers['Location'] = url_for('api.get_hero', id=hero.id)
    return response

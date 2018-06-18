import datetime
import random
import itertools
from collections import OrderedDict

import jwt

from . import api, errors, decorators
from flask import request, jsonify, url_for, make_response, current_app
from app.models import Hero, Permission, GroupType, Group, Fight
from app import db


@api.route('/ranking')
def ranking():
    # martwy bohater nie liczy sie do rankingu
    heroes = Hero.query.filter(Hero.health > 0).filter(Hero.is_participant.is_(True))

    output = []

    for hero in heroes:
        walki_hero_lost =  Fight.query.filter_by(beaten_name=hero.name).count()
        walki_hero_won = Fight.query.filter_by(winner_name=hero.name).count()
        if walki_hero_lost == 0 and walki_hero_won == 0:
            continue
        output.append({'name': hero.name, 'wygranych': walki_hero_won, 'przegranych': walki_hero_lost})

    return jsonify(output)


@api.route('/deaths')
def polegli():

    polegli_lista = Fight.query.filter(Fight.killed == 1)

    output = []

    for polegly in polegli_lista:
        ilosc_wygranych_lista = Fight.query.filter(Fight.winner_name == polegly.beaten_name).count()
        output.append((ilosc_wygranych_lista, {'name': polegly.beaten_name, 'date': polegly.date, 'ilosc wygranych': ilosc_wygranych_lista}))

    result = sorted(output, key=lambda tup: tup[0], reverse=True)
    return jsonify([i[1] for i in result])


###########################
# REMEMBER TO ADD PROPER DATA VALIDATION / cerberus
###########################


@api.route('/heroes/<public_id>', methods=['PATCH'])
def kill_hero(public_id):
    hero = Hero.query.filter_by(public_id=public_id).first()

    if not hero:
        return errors.bad_request('No hero found')

    hero.is_participant = False
    hero.health = 0
    db.session.add(hero)
    db.session.commit()

    return jsonify({}), 204


@api.route('/heroes/<public_id>', methods=['DELETE'])
def delete_hero(public_id):

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
    response.headers['Location'] = url_for('api.get_hero', public_id=hero.public_id)
    return response


@api.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    hero = Hero.query.filter_by(name=auth.username).first()

    if not hero:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if hero.check_password(auth.password):
        token = jwt.encode({
            'public_id': hero.public_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
            }, current_app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


# UGLY CODE, TO REFACTOR TODAY

@api.route('/fights', methods=['POST'])
# @decorators.token_required
# @decorators.grandmaster_required
def add_fight():
    heroes = Hero.query.filter(Hero.health > 0).filter(Hero.is_participant.is_(True))

    output = []

    for hero in heroes:
        output.append(hero)

    random.shuffle(output)

    output2 = list(itertools.combinations(output, 2))

    for hero1, hero2 in output2:
        hero1_enemies = Group.query.filter_by(type=hero1.group_id).first()
        hero2_enemies = Group.query.filter_by(type=hero2.group_id).first()
        if hero1.can_fight_with(hero1_enemies.enemies) or hero2.can_fight_with(hero2_enemies.enemies):
            winner = random.choice([hero1.name, hero2.name])
            looser = ""
            if winner == hero1.name:
                looser = hero2
            else:
                looser = hero1

            looser.health = looser.health - random.randint(1, 100)

            fight = Fight(winner_name=winner, beaten_name=looser.name, killed=looser.health < 0,
                          date=datetime.datetime.utcnow())
            db.session.add(fight)
            db.session.commit()
            return jsonify(fight.to_dict())
    return jsonify({'error': 'There is no characters to fight'})
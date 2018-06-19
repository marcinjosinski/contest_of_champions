import datetime
import random
import itertools

from sqlalchemy import and_

from . import api, decorators
from flask import jsonify
from app.models import Hero, Group, Fight
from app import db


@api.route('/ranking')
@decorators.token_required
def ranking_list(current_hero):
    alive_heroes = Hero.query.filter(Hero.health > 0).filter(Hero.is_participant.is_(True))

    output = []
    for hero in alive_heroes:
        winner_fights =  Fight.query.filter_by(beaten_name=hero.name).count()
        beaten_fights = Fight.query.filter_by(winner_name=hero.name).count()
        if winner_fights == 0 and beaten_fights == 0:
            continue
        output.append({
            'name': hero.name,
            'won': winner_fights,
            'lost': beaten_fights
        })

    return jsonify(output)


@api.route('/deaths')
@decorators.token_required
@decorators.grandmaster_required
def deaths_list(current_hero):

    death_list = Fight.query.filter(Fight.killed == 1)

    output = []
    for dead in death_list:
        win_count = Fight.query.filter(Fight.winner_name == dead.beaten_name).count()
        output.append((win_count,
                       {'name': dead.beaten_name,
                        'date': dead.date
                        }))

    result = sorted(output, key=lambda tup: tup[0], reverse=True)
    return jsonify([i[1] for i in result])


@api.route('/fights', methods=['POST'])
@decorators.token_required
@decorators.grandmaster_required
def add_fight(current_hero):
    heroes = Hero.query.filter(Hero.health > 0).filter(Hero.is_participant.is_(True))

    heroes_list = []
    for hero in heroes:
        heroes_list.append(hero)

    # Really straight forward duel algorithm

    random.shuffle(heroes_list)

    pair_combinations = list(itertools.combinations(heroes_list, 2))

    for hero1, hero2 in pair_combinations:
        hero1_enemies = Group.query.filter_by(type=hero1.group_id).first()
        hero2_enemies = Group.query.filter_by(type=hero2.group_id).first()

        if hero1.can_fight_with(hero1_enemies.enemies) or hero2.can_fight_with(hero2_enemies.enemies):
            f1 = Fight.query.filter(and_(Fight.winner_name == hero1.name, Fight.beaten_name == hero2.name)).first()
            f2 = Fight.query.filter(and_(Fight.winner_name == hero2.name, Fight.beaten_name == hero1.name)).first()

            if f1 is not None or f2 is not None:
                continue

            winner = random.choice([hero1.name, hero2.name])
            beaten = hero1 if winner == hero2.name else hero2
            beaten.health = beaten.health - random.randint(1, 100)

            fight = Fight(winner_name=winner, beaten_name=beaten.name, killed=beaten.health < 0,
                          date=datetime.datetime.utcnow())

            db.session.add(fight)
            db.session.commit()

            return jsonify(fight.to_dict())
    return jsonify({'error': 'There is no characters to fight'})




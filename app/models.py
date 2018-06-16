import enum
from . import db
from datetime import datetime


class Permission:
    NORMAL = 1
    ADMIN = 2


class GroupType(enum.IntEnum):
    NONE = 0
    HUMAN = 1
    MYSTIC = 2
    MUTANT = 4

    def __str__(self):
        return str(self.name)


class Hero(db.Model):
    __tablename__ = 'heroes'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(32), unique=True, index=True)
    password_hash = db.Column(db.String(128), index=True)
    health = db.Column(db.Integer, default=100)
    permissions = db.Column(db.Integer, default=Permission.NORMAL)
    group_id = db.Column(db.Enum(GroupType), db.ForeignKey('groups.type'))
    is_participant = db.Column(db.Boolean, default=True)



class Group(db.Model):
    __tablename__ = 'groups'
    type = db.Column(db.Enum(GroupType), primary_key=True)
    enemies = db.Column(db.Integer)
    heroes = db.relationship('Hero', backref='group', lazy=True)

    @staticmethod
    def establish_enemies():
        enemies = {
            'HUMAN': GroupType.MYSTIC | GroupType.MUTANT,
            'MYSTIC': GroupType.HUMAN,
            'MUTANT': GroupType.HUMAN | GroupType.MUTANT,
        }

        for group_name, enemies_list in enemies.items():
            query = Group.query.filter_by(type=GroupType[group_name]).all()
            for group in query:
                group.enemies = int(enemies_list)
                db.session.add(group)
        db.session.commit()


class Fight(db.Model):
    __tablename__ = 'fights'
    id = db.Column(db.Integer, primary_key=True)
    winner_name = db.Column(db.String(32), index=True, nullable=False)
    beaten_name = db.Column(db.String(32), index=True, nullable=False)
    killed = db.Column(db.Boolean, index=True, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
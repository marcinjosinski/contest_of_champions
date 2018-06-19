from functools import wraps

import jwt
from flask import request, current_app, g

from app.models import Hero, Permission
from . import errors


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return errors.unauthorized('Token is missing')

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            hero = Hero.query.filter_by(public_id=data['public_id']).first()

            g.current_hero = hero

        except jwt.ExpiredSignatureError:
            return errors.unauthorized('Signature has expired')
        except:
            return errors.unauthorized('Token is invalid')

        return f(hero, *args, **kwargs)

    return decorated


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if g.current_hero.permissions != permission:
                return errors.unauthorized('You do not have permissions to look here')
            return f(*args, **kwargs)
        return decorated
    return decorator


def grandmaster_required(f):
    return permission_required(Permission.ADMIN)(f)

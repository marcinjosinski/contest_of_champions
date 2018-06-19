import datetime
import jwt

from . import api, errors
from flask import request, jsonify, make_response, current_app
from app.models import Hero


@api.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return errors.login_required('Could not verify. Do not forget about username and password')

    hero = Hero.query.filter_by(name=auth.username).first()

    if not hero:
        return errors.login_required('Could not verify. There is no such hero')

    if hero.check_password(auth.password):
        token = jwt.encode({
            'public_id': hero.public_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
            }, current_app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})

    return errors.login_required('Sorry, something went wrong')

from flask import jsonify


def bad_request(message):
    response = jsonify({
        'error': 'bad request',
        'message': message
    })
    return response


def unauthorized(message):
    response = jsonify({
        'error': 'unauthorized',
        'message': message
    })
    return response

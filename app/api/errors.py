from flask import jsonify


def bad_request(message):
    response = jsonify({
        'error': 'bad request',
        'message': message
    })
    response.status_code = 400
    return response


def unauthorized(message):
    response = jsonify({
        'error': 'unauthorized',
        'message': message
    })
    response.status_code = 401
    return response


def login_required(message):
    response = jsonify({'error': message})
    response.headers = {
        'WWW-Authenticate': 'Basic realm="Login required!"',
        'Content-Type': 'application/json'
    }
    response.status_code = 401
    return response

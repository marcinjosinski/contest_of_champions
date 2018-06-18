from base64 import b64encode

from flask import json


def test_valid_login(test_client):
    """
    GIVEN a flask application
    WHEN the '/login' page is requested (GET)
    THEN check the response is valid
    """
    headers = {
        'Authorization': 'Basic ' + b64encode(
            ('Grandmaster' + ':' + 'Haslo').encode('utf-8')).decode('utf-8'),
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = test_client.get('/login',
                               headers=headers)
    assert response.status_code == 200
    assert b'token' in response.data


def test_404(test_client):
    response = test_client.get('/wrong/url')
    json_response = json.loads(response.get_data(as_text=True))

    assert response.status_code == 404
    assert json_response['error'] == 'not found'

from . import api


@api.route('/ranking')
def ranking():
    return 'Works'

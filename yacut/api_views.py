from flask import jsonify, request, url_for

from . import app
from .error_handlers import InvalidAPIUsage
from .services import ShortLinkService


@app.route('/api/id/', methods=['POST'])
def api_create_short_link():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса', 400)
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!', 400)

    try:
        url_map = ShortLinkService.create_short_link(
            original_url=data['url'],
            custom_id=data.get('custom_id')
        )
    except ShortLinkService.ShortLinkError as e:
        raise InvalidAPIUsage(str(e), 400)

    return (
        jsonify(
            {
                'url': url_map.original,
                'short_link': url_for(
                    'mapping_redirect',
                    short_id=url_map.short,
                    _external=True,
                ),
            }
        ),
        201
    )


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def api_get_original_link(short_id):
    try:
        original_url = ShortLinkService.get_original_url(short_id)
    except ShortLinkService.ShortLinkError as e:
        raise InvalidAPIUsage(str(e), 404)
    return jsonify({'url': original_url}), 200
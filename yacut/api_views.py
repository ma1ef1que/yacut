import re

from flask import jsonify, request, url_for

from . import app, db
from .constants import PATTERN
from .utils import get_unique_short_id
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def api_create_short_link():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса', 400)
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!', 400)
    custom_id = data.get('custom_id', '')
    if custom_id:
        if URLMap.query.filter_by(short=custom_id).first():
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.', 400)
        if not re.match(PATTERN, custom_id):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки', 400)
    else:
        data['custom_id'] = get_unique_short_id()

    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()

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
        ), 201
    )


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def api_get_original_link(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({
        'url': url_map.original,
    }), 200
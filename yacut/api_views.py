import re
from http import HTTPStatus

from flask import jsonify, request

from yacut import app, db
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URL_map
from yacut.utils import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def get_new_url():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    short_id = data.get('custom_id')
    if short_id:
        if not (
            len(short_id) <= 16 and
            isinstance(short_id, str) and
            re.match(r'^[A-Za-z0-9]*$', short_id)
        ):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )
        if URL_map.query.filter_by(short=short_id).first():
            raise InvalidAPIUsage(f'Имя "{short_id}" уже занято.')
    if short_id is None or short_id == '':
        short_id = get_unique_short_id()
    url = URL_map(
        original=data.get('url'),
        short=short_id
    )
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict_full()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url_by_short_id(short_id):
    redirect_url = URL_map.query.filter_by(short=short_id).first()
    if redirect_url is None:
        raise InvalidAPIUsage(
            'Указанный id не найден', HTTPStatus.NOT_FOUND
        )
    return jsonify(redirect_url.to_dict_short()), HTTPStatus.OK

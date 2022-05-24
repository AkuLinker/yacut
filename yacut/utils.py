import random
import string

from yacut.models import URL_map


def get_unique_short_id():
    characters = string.ascii_letters + string.digits
    short_id = ''.join(random.choice(characters) for _ in range(6))
    if URL_map.query.filter_by(short=short_id).first():
        short_id = get_unique_short_id()
    return short_id

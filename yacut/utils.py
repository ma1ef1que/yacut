import random

from .models import URLMap
from .constants import CHARACTERS


def get_unique_short_id(length=6):
    while True:
        short_id = ''.join(random.choice(CHARACTERS)
                           for _ in range(length))

        if not URLMap.query.filter_by(short=short_id).first():
            return short_id


def check_unique_short_id(short_id):
    if not short_id:
        return False
    return not URLMap.query.filter_by(short=short_id).first()

import re
from typing import Optional
import random

import validators

from .constants import PATTERN, SHORT_ID_LENGTH, MAX_URL_LENGTH, CHARACTERS
from .models import URLMap
from . import db


class ShortLinkService:
    class ShortLinkError(Exception):
        """Базовое исключение для ошибок бизнес-логики."""
        pass

    class InvalidShortIdError(ShortLinkError):
        """Исключение для некорректного формата короткой ссылки."""
        pass

    class ShortIdExistsError(ShortLinkError):
        """Исключение для уже существующей короткой ссылки."""
        pass

    @staticmethod
    def validate_short_id(short_id: str) -> None:
        """Проверяет формат и длину короткой ссылки."""
        if not short_id:
            return
        if len(short_id) > SHORT_ID_LENGTH:
            raise ShortLinkService.InvalidShortIdError(
                'Указано недопустимое имя для короткой ссылки'
            )
        if not re.match(PATTERN, short_id):
            raise ShortLinkService.InvalidShortIdError(
                'Указано недопустимое имя для короткой ссылки'
            )

    @staticmethod
    def check_unique_short_id(short_id: str) -> None:
        """Проверяет уникальность короткой ссылки."""
        if URLMap.query.filter_by(short=short_id).first():
            raise ShortLinkService.ShortIdExistsError(
                'Предложенный вариант короткой ссылки уже существует.'
            )

    @staticmethod
    def get_unique_short_id(length: int = SHORT_ID_LENGTH) -> str:
        """Генерирует уникальный короткий идентификатор."""
        while True:
            short_id = ''.join(random.choice(CHARACTERS)
                               for _ in range(length))
            try:
                ShortLinkService.check_unique_short_id(short_id)
                return short_id
            except ShortLinkService.ShortIdExistsError:
                continue

    @staticmethod
    def create_short_link(
            original_url: str, custom_id: Optional[str] = None) -> URLMap:
        """Создает новую короткую ссылку."""
        if not validators.url(original_url):
            raise ShortLinkService.ShortLinkError('Некорректный URL')
        if len(original_url) > MAX_URL_LENGTH:
            raise ShortLinkService.ShortLinkError('URL слишком длинный')
        if custom_id:
            ShortLinkService.validate_short_id(custom_id)
            ShortLinkService.check_unique_short_id(custom_id)
        else:
            custom_id = ShortLinkService.get_unique_short_id()

        url_map = URLMap(original=original_url, short=custom_id)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def get_original_url(short_id: str) -> str:
        """Получает оригинальный URL по короткой ссылке."""
        url_map = URLMap.query.filter_by(short=short_id).first()
        if not url_map:
            raise ShortLinkService.ShortLinkError('Указанный id не найден')
        return url_map.original

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, URL, Regexp, Optional

from .constants import PATTERN, SHORT_ID_LENGTH


class URLForm(FlaskForm):
    original_link = StringField(
        'Введите ссылку',
        validators=[
            DataRequired(message='Обязательное поле'),
            URL(message='Некорректная ссылка'),
            Length(max=2000, message='URL слишком длинный')
        ],
    )
    custom_id = StringField(
        'Введите короткую ссылку',
        validators=[
            Optional(),
            Length(max=SHORT_ID_LENGTH,
                   message='Указано недопустимое имя для короткой ссылки'),
            Regexp(PATTERN, message='Только латиница и цифры'),
        ],
    )
    submit = SubmitField('Сократить')

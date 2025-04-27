from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, URL, Optional

from .constants import MAX_URL_LENGTH


class URLForm(FlaskForm):
    original_link = StringField(
        'Введите ссылку',
        validators=[
            DataRequired(message='Обязательное поле'),
            URL(message='Некорректная ссылка'),
            Length(max=MAX_URL_LENGTH, message='URL слишком длинный')
        ],
    )
    custom_id = StringField(
        'Введите короткую ссылку',
        validators=[Optional()],
    )
    submit = SubmitField('Сократить')

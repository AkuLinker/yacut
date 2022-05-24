from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional


class URLForm(FlaskForm):
    original_link = URLField(
        'Оригинальная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    URL(message='Ссылка некорректна')]
    )
    custom_id = StringField(
        'Кастомная ссылка',
        validators=[Length(1, 16), Optional()]
    )
    submit = SubmitField('Создать')

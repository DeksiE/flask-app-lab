
from decimal import Decimal

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, TextAreaField, DecimalField,
    SelectField, IntegerField, SubmitField
)
from wtforms.validators import (
    DataRequired, InputRequired, Length,
    NumberRange, Optional, ValidationError
)


class ProductForm(FlaskForm):
    name = StringField(
        'Назва товару',
        validators=[
            DataRequired(),
            Length(min=3, message='Мінімум 3 символи')
        ]
    )

    content = TextAreaField(
        'Опис товару',
        validators=[DataRequired()],
        render_kw={'rows': 5, 'cols': 40}
    )

    price = DecimalField(
        'Ціна',
        places=2,
        validators=[
            DataRequired(),
            NumberRange(min=Decimal('0.01'), message='Ціна має бути додатною')
        ]
    )

    category = SelectField(
        'Категорія',
        choices=[
            ('laptops', 'Ноутбуки'),
            ('phones', 'Телефони'),
            ('computers', 'Комп’ютери'),
            ('other', 'Інше')
        ],
        validators=[DataRequired()]
    )

    quantity = IntegerField(
        'Кількість',
        validators=[
            InputRequired(message='Введіть кількість'),
            NumberRange(min=0, message='Кількість не може бути від’ємною')
        ]
    )

    image = FileField(
        'Зображення товару',
        validators=[
            Optional(),
            FileAllowed(['jpg', 'jpeg', 'png'], 'Дозволені лише JPG, JPEG та PNG')
        ]
    )

    submit = SubmitField('Зберегти товар')

    def validate_price(self, field):
        if field.data is not None:
            if field.data.as_tuple().exponent < -2:
                raise ValidationError('Максимум 2 знаки після коми')

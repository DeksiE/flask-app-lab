
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp


class ContactForm(FlaskForm):
    name = StringField(
        'Ім’я',
        validators=[
            DataRequired(message='Введіть ім’я'),
            Length(min=4, max=10, message='Ім’я повинно містити від 4 до 10 символів')
        ]
    )

    email = StringField(
        'Email',
        validators=[
            DataRequired(message='Введіть email'),
            Email(message='Некоректна електронна адреса')
        ]
    )

    phone = StringField(
        'Телефон',
        validators=[
            DataRequired(message='Введіть номер телефону'),
            Regexp(
                r'^\+380\d{9}$',
                message='Формат телефону: +380XXXXXXXXX'
            )
        ]
    )

    subject = SelectField(
        'Тема повідомлення',
        choices=[
            ('', 'Оберіть тему'),
            ('question', 'Запитання'),
            ('cooperation', 'Співпраця'),
            ('feedback', 'Відгук')
        ],
        validators=[DataRequired(message='Оберіть тему повідомлення')]
    )

    message = TextAreaField(
        'Повідомлення',
        validators=[
            DataRequired(message='Введіть повідомлення'),
            Length(max=500, message='Максимум 500 символів')
        ],
        render_kw={'rows': 5, 'cols': 40}
    )

    submit = SubmitField('Надіслати повідомлення')

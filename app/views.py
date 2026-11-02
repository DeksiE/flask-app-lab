import logging
from pathlib import Path
from decimal import Decimal

from flask import render_template, redirect, url_for, flash
from . import app
from .forms import ContactForm

@app.route('/')
@app.route('/resume')
def resume():
    return render_template('resume.html', title='Резюме')


@app.route('/contacts', methods=['GET', 'POST'])
@app.route('/contact', methods=['GET', 'POST'])
def contacts():
    form = ContactForm()

    if form.validate_on_submit():
        try:
            log_dir = Path(app.root_path).parent / 'logs'
            log_dir.mkdir(exist_ok=True)

            logging.basicConfig(
                filename=log_dir / 'contacts.log',
                level=logging.INFO,
                format='%(asctime)s - %(message)s'
            )

            logger = logging.getLogger('contacts')
            logger.setLevel(logging.INFO)

            if not logger.handlers:
                handler = logging.FileHandler(
                    log_dir / 'contacts.log',
                    encoding='utf-8'
                )
                handler.setFormatter(
                    logging.Formatter('%(asctime)s - %(message)s')
                )
                logger.addHandler(handler)

            logger.info(
                'Name: %s | Email: %s | Phone: %s | Subject: %s | Message: %s',
                form.name.data,
                form.email.data,
                form.phone.data,
                form.subject.data,
                form.message.data
            )

            flash('Повідомлення успішно збережено!', 'success')

        except OSError:
            flash('Помилка збереження повідомлення!', 'danger')

        return redirect(url_for('contacts'))

    if form.is_submitted() and form.errors:
        flash('Перевірте правильність заповнення форми.', 'danger')

    return render_template(
        'contacts.html',
        title='Контакти',
        form=form
    )

@app.route('/homepage')
def home():
    return render_template('homepage.html', title='Головна сторінка')
from flask import render_template
from . import app

@app.route('/')
@app.route('/resume')
def resume():
    return render_template('resume.html', title='Резюме')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title='Контакти')

@app.route('/homepage')
def home():
    return render_template('homepage.html', title='Головна сторінка')
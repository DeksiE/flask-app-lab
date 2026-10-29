from flask import render_template, request, redirect, url_for, session, flash, make_response
from . import users_bp

@users_bp.route('/hi/<name>')
def greetings(name):
    age = request.args.get('age', type=int)
    return render_template(
        'users/hi.html',
        title='Привітання',
        name=name,
        age=age
    )

@users_bp.route('/admin')
def admin():
    return redirect(url_for('users.greetings', name='administrator', age=45))

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin' and password == '12345':
            session['username'] = username
            flash('Вхід виконано успішно!', 'success')
            return redirect(url_for('users.profile'))

        flash('Неправильний логін або пароль!', 'danger')
        return redirect(url_for('users.login'))

    return render_template('users/login.html', title='Вхід')


@users_bp.route('/profile')
def profile():
    username = session.get('username')

    if not username:
        flash('Спочатку увійдіть у систему!', 'danger')
        return redirect(url_for('users.login'))

    cookies = {
        key: value
        for key, value in request.cookies.items()
        if key != 'session'
    }

    theme = request.cookies.get('theme', 'light')

    if theme not in ['light', 'dark']:
        theme = 'light'

    return render_template(
        'users/profile.html',
        title='Профіль',
        username=username,
        cookies=cookies,
        theme=theme
    )


@users_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    flash('Ви вийшли із системи.', 'info')
    return redirect(url_for('users.login'))

@users_bp.route('/cookies/add', methods=['POST'])
def add_cookie():
    if 'username' not in session:
        return redirect(url_for('users.login'))

    key = request.form.get('key', '').strip()
    value = request.form.get('value', '')
    max_age = request.form.get('max_age', 3600, type=int)

    if not key or key.lower() == 'session':
        flash('Некоректна або зарезервована назва кукі!', 'danger')
        return redirect(url_for('users.profile'))

    response = make_response(redirect(url_for('users.profile')))
    response.set_cookie(key, value, max_age=max_age)

    flash('Кукі успішно додано!', 'success')
    return response


@users_bp.route('/cookies/delete', methods=['POST'])
def delete_cookie():
    if 'username' not in session:
        return redirect(url_for('users.login'))

    key = request.form.get('key', '').strip()

    if not key or key.lower() == 'session':
        flash('Некоректна або зарезервована назва кукі!', 'danger')
        return redirect(url_for('users.profile'))

    response = make_response(redirect(url_for('users.profile')))
    response.delete_cookie(key)

    flash('Кукі видалено!', 'success')
    return response


@users_bp.route('/cookies/delete-all', methods=['POST'])
def delete_all_cookies():
    if 'username' not in session:
        return redirect(url_for('users.login'))

    response = make_response(redirect(url_for('users.profile')))

    for key in request.cookies:
        if key != 'session':
            response.delete_cookie(key)

    flash('Кукі видалено!', 'success')
    return response

@users_bp.route('/theme/<theme>', methods=['POST'])
def change_theme(theme):
    if 'username' not in session:
        flash('Спочатку увійдіть у систему!', 'danger')
        return redirect(url_for('users.login'))

    if theme not in ['light', 'dark']:
        flash('Невідома тема!', 'danger')
        return redirect(url_for('users.profile'))

    response = make_response(redirect(url_for('users.profile')))
    response.set_cookie('theme', theme, max_age=30 * 24 * 60 * 60)

    flash('Кольорову схему змінено!', 'success')
    return response
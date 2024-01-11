from flask import render_template, redirect, url_for, request, flash, session
from forms import UserRegistrationForm, UserLoginForm
from app import app, db
from models import User

from functools import wraps


bad_user_agents = [
    'request',
    'robot',
    'spider',
    'scrapy',
    'crawl',
    'parser'
]


def login_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if 'user_id' in session and User.query.get(session.get('user_id')):
            return f(*args, **kwargs)

        return redirect(url_for('register'))

    return inner


def subscription_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        # TODO: do some check stuff
        if 'user_id' in session and User.get(session.get('user_id')).first():
            return f(*args, **kwargs)

        return redirect(url_for('subscriptions'))

    return inner


@app.before_request
def check_user_agent():
    user_agent = request.headers.get('User-Agent')

    if not user_agent:
        return '<h1>Hi Bot! Check your cookies</h1><h2>If you are seeing this and you are a human, enable JavaScript and refresh your cookeis :D</h2>'

    for bad_user_agent in bad_user_agents:
        if bad_user_agent in user_agent.lower():
            return '<h1>Hi Bot! Check your cookies</h1><h2>If you are seeing this and you are a human, enable JavaScript and refresh your cookeis :D</h2>'


@app.route('/main')
@app.route('/')
def main():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegistrationForm()
    print(f'Form errors: {form.errors}')

    if request.method == 'GET':
        return render_template('register.html', form=form)

    else:
        if form.validate_on_submit():
            user = User.create(
                form.password.data,
                username=form.username.data,
                last_name=form.last_name.data,
                first_name=form.first_name.data,
            )
            if user:
                session['user_id'] = user.id
                session['username'] = user.username
                return redirect(url_for('main'))

        flash('Registration failed: this username is already taken or password do not match', 'danger')
        return redirect(url_for('register'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()

    if request.method == 'GET':
        return render_template('login.html', form=form)

    if form.validate_on_submit():
        user = User.validate_user(form.username.data, form.password.data)
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('main'))

    flash('Username or/and password do not match', 'warning')
    return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('main'))


@app.route('/profile')
@login_required
def profile():
    username = session.get('username')
    return f'Hi {username}!'


@app.route('/generate')
@login_required
@subscription_required
def generate_leads():
    user_id = session.get('user_id')
    return f'Hi User #{user_id}, wanna generate some leads?'


@app.route('/subscriptions')
def subscriptions():
    return render_template('subscriptions.html')


@app.errorhandler(404)
def error(e):
    return render_template('error.html', error=e), 404

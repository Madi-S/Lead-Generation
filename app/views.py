from flask import render_template, redirect, url_for, request, session
from app import app, db, recaptcha
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
        if 'user_id' in session and User.get(session.get('user_id')).first():
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


@app.route('/register')
def register():
    # if recaptcha.verify():
    # session['user_id'] = user.id
    return render_template('register.html')


@app.route('/profile')
@login_required
def profile():
    user_id = session.get('user_id')
    return f'Hi User #{user_id}'


@app.route('/generate')
@login_required
@subscription_required
def generate_leads():
    user_id = session.get('user_id')
    return f'Hi User #{user_id}, wanna generate some leads?'


@app.route('/subscriptions')
def subscriptions():
    return 'Subscriptions here'


@app.errorhandler(404)
def error(e):
    return render_template('error.html', error=e), 404
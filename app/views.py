from flask import render_template, redirect, url_for, request
from app import app

bad_user_agents = [
    'request',
    'robot',
    'spider',
    'scrapy',
    'crawl',
    'parser'
]

@app.before_request
def check_user_agent():    
    user_agent = request.headers.get('User-Agent')
    
    if not user_agent:
        return '<h1>Hi Bot! Check your cookies</h1><h2>If you are seeing this and you are a human, enable JavaScript and refresh your cookeis :D</h2>'

    for bad_user_agent in bad_user_agents:
        if bad_user_agent in user_agent.lower():
            return '<h1>Hi Bot! Check your cookies</h1><h2>If you are seeing this and you are a human, enable JavaScript and refresh your cookeis :D</h2>'


@app.route('/main')
def main():
    return render_template('index.html')


@app.errorhandler(404)
def error(e):
    return render_template('errors/not_found.html', error=e), 404
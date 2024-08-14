from flask import Flask, request, render_template, redirect, url_for
import asyncio
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run():
    search_query = request.form.get('topic')
    location = request.form.get('location')

    # Save form data to a file or directly pass to the script
    # For this example, we assume the form data is written to a temporary file or environment variables
    # You can also directly modify the run.py script to use these variables

    # Call the run.py script with the form data
    # This is a placeholder for how you'd integrate with your script
    subprocess.run([
        'python', 'run.py',
        '--search_query', search_query,
        '--location', location,
    ], check=True)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

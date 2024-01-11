from flask import Flask
from flask_migrate import Migrate
from flask_recaptcha import ReCaptcha
from flask_sqlalchemy import SQLAlchemy

from config import Config


app = Flask('Lead Generation')

app.config.from_object(Config)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

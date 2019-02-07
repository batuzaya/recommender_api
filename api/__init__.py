# Application
from flask import Flask
from api.config import *

app = Flask(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# Database
from flask_sqlalchemy import SQLAlchemy

# Environment
from os import getenv

if getenv('ENV') == 'production':
    config = ProductionConfig()
else:
    config = DevelopmentConfig()

app.config.from_object(config)

db = SQLAlchemy(app)

# Import the controllers
from .controllers.rankingController import RankingController
from .models import ranking

import MySQLdb
from os import getenv
from daemon.config import *

if getenv('FLASK_ENV') == 'production':
    config = ProductionConfig()
else:
    config = DevelopmentConfig()

remote_db = MySQLdb.connect(host=config.db_host,
                     user=config.db_username,
                     passwd=config.db_password,
                     db=config.db_name)
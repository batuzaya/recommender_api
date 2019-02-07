# Recommender App

The system consists of two parts: api and daemon.


How to set up API
=================
For local development setup:
```bash
    # Setup and activate virtualenv
    virtualenv .venv
    source ./.venv/bin/activate

    # Install the pip requirements
    pip install -r requirements.txt

    # Create the development database
    python manage.py database migrate upgrade

    # Start the application, prefixing with the required environment variables
    DATABASE_URL=mysql://user:password@localhost/dbname python server.py
```

When deploying to production, ensure the following environment variables are set:

* `FLASK_ENV` - Must be set to "production". Used to switch to the production configuration.
* `SECRET_KEY` - Must be a random hash. Used by to generate secure session hashes.
* `PORT` - The port to run the application on. Defaults to 5000.

Next, run the `migrate upgrade` like you did locally:

* `python manage.py database migrate upgrade`

How to set up daemon
====================
Open the configuration file daemon/config.py and configure the database connection:
```bash
class Config(object):
    port = 3306

class ProductionConfig(Config):
    db_host = ""
    db_username = ""
    db_password = ""
    db_name = ""

class DevelopmentConfig(Config):
    db_host = "localhost"
    db_username = "root"
    db_password = "123456789"
    db_name = "joe_db"

```
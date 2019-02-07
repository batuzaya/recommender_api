# Recommender App

The system consists of two parts: api and daemon.
The daemon is expected to run once a day to rankify recommended items for each user.
The api runs based on the result from this daemon.

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

* `ENV` - Must be set to "production". Used to switch to the production configuration.
* `SECRET_KEY` - Must be a random hash. Used by to generate secure session hashes.
* `PORT` - The port to run the application on. Defaults to 5000.

Next, run the `migrate upgrade` like you did locally:

* `python manage.py database migrate upgrade`

How to set up daemon
====================
The daemon needs to connect to the remote database in order to read orders.
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
Along with the remote database, the daemon also uses the same local database as the API to store results.

When deploying to production, ensure the following environment variables are set:

* `ENV` - Must be set to "production". Used to switch to the production configuration.

API specs
=========
The api has 3 endpoints:
* `/api/segmentation` - Returns RFM classes of all users as in the following format.
```bash
    [
        {
            "F_Quartile": 2,
            "M_Quartile": 3,
            "RFMClass": "423",
            "R_Quartile": 4,
            "user_id": 1
        },
        ...
    ]
```
* `/api/segmentation/<int:user_id>` - Returns a RFM class for the user as in the following format.
```bash
    {
        "F_Quartile": 2,
        "M_Quartile": 3,
        "RFMClass": "423",
        "R_Quartile": 4
    }
```
* `/api/ranking/<int:user_id>` - Returns the top 5 recommended items for the user.
```bash
    {
        "items": [
            {
                "item_id": 12,
                "user_id": 1
            },
            {
                "item_id": 14,
                "user_id": 1
            },
            {
                "item_id": 32,
                "user_id": 1
            },
            {
                "item_id": 48,
                "user_id": 1
            },
            {
                "item_id": 60,
                "user_id": 1
            }
        ],
        "success": 1
    }
```
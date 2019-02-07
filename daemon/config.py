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

class Config(object):
    SECRET_KEY = '79ad44ee992827e18c81f34a553a85fb'

class Proconfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True 
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"

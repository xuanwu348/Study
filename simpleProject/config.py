class Config(object):
    pass

class Proconfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True 
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"

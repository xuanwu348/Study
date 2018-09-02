class Config(object):
    pass

class Proconfig(Config):
    pass

class DevConfig(Config):
    Debug = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"

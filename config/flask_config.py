class BaseConfig(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(BaseConfig):    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SERVER = "Production"

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SERVER = "Development"


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True



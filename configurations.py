class BaseConfig(object):
    DEBUG = True
    TESTING = False


class ProductionConfig(BaseConfig):
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True

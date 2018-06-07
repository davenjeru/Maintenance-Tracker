import os


class Config(object):
    """Parent configuration class"""
    DEBUG = False
    JWT_TOKEN_LOCATION = 'headers'
    JWT_HEADER_NAME = 'ACCESS_TOKEN'
    JWT_HEADER_TYPE = ''
    JWT_BLACKLIST_ENABLED = True


class Development(Config):
    """ Development Configurations"""
    DEBUG = True
    SECRET_KEY = 'developmentsecretkey'


class Production(Config):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY')


class Testing(Config):
    TESTING = True
    DEBUG = True
    SECRET_KEY = 'testingsecretkey'


class Staging(Config):
    DEBUG = False


app_config = {
    'development': Development,
    'production': Production,
    'staging': Staging,
    'testing': Testing
}

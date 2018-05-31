class Config(object):
    """Parent configuration class"""
    DEBUG = False


class Development(Config):
    """ Development Configurations"""
    DEBUG = True
    SECRET_KEY = 'developmentsecretkey'


class Production(Config):
    DEBUG = False
    TESTING = False


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

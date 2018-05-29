class Config(object):
    """Parent configuration class"""
    DEBUG = False


class Development(Config):
    """ Development Configurations"""
    DEBUG = True


class Production(Config):
    DEBUG = False
    TESTING = False


class Testing(Config):
    TESTING = True
    DEBUG = True


class Staging(Config):
    DEBUG = False


app_config = {
    'development': Development,
    'production': Production,
    'staging': Staging,
    'testing': Testing
}

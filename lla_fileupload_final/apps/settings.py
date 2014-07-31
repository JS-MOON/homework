class Config(object):
    debug = False


class Production(Config):
    DEBUG = True
    ADMIN = "lla@lla.com"
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024

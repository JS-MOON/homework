class Config(object):
    debug = False


class Production(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = False
    ADMIN = "ckc6842@gmail.com"
    SECRET_KEY = "1234"
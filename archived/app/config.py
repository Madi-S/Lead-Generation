from datetime import timedelta
from sys import platform


class Config(object):
    DEBUG = True

    WTF_CSRF_SECRET_KEY = 'a random string'

    SECRET_KEY = '6554410059521c8b5426eba21e54a7a193aaf30e67645e8c24a2f6eb8779790711a4ca0b9d62ef43e79caddf1e5a123808a4ea370f69c59cd64003e1c9ac8659'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    if platform.startswith('w'):
        # For Windows
        SQLALCHEMY_DATABASE_URI = r'sqlite:///C:\Users\khova\Desktop\Python\Code\Lead Generation\Lead-Generation\app\db\lg.db'

    else:
        # For Ubuntu
        SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:1234@localhost/lg'

    SESSION_TYPE = 'redis'  # redis, memcached, filesystem or mongodb
    PERMANENT_SESSION_LIFETIME = timedelta(days=90)

    RECAPTCHA_PUBLIC_KEY = '6LeENmoaAAAAAH1dMElRkLRGE2UiSP-CK831656U'
    RECAPTCHA_PRIVATE_KEY = '6LeENmoaAAAAANfgmGgA9Of_IPlJWtppMLMoMoV4'
    # RECAPTCHA_THEME = 'dark'
    # RECAPTCHA_TYPE = 'audio'
    # RECAPTCHA_SIZE = 'compact'

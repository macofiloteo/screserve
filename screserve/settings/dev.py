from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


SECRET_KEY = 'r&-gaknsp&6n34%zw3!kh)%^=t-@p(orgposdm@our2i$7_v3('

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


try:
    from .local import *
except ImportError:
    pass

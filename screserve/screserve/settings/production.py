from .base import *

DEBUG = True

SECRET_KEY = 'r&-gaknsp&6n34%zw3!kh)%^=t-@p(orgposdm@our2i$7_v3('

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'screserve',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

try:
    from .local import *
except ImportError:
    pass

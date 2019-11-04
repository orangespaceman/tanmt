# Test env - used for local test runner

from .app import *  # noqa
from .env import *  # noqa

# Config settings below are manually set here rather than via .env file as
# these tests are generally run while the default .env is active

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django_test',
        'USER': '',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
    }
}

SITE_URL = 'http://example.com'

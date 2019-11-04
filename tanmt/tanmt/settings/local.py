# Local env - used for development

from .app import *  # noqa
from .env import *  # noqa

INSTALLED_APPS += [  # noqa
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE  # noqa

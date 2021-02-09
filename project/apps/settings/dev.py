from .common import *  # noqa
from django.utils.translation import gettext_lazy as _

ALLOWED_HOSTS = ['*']
DEBUG = True
SECRET_KEY = 'not-a-valid-secret-key'

INSTALLED_APPS += (
    'debug_toolbar',
    'rosetta',
)
CORS_ORIGIN_ALLOW_ALL = env('CORS_ORIGIN_ALLOW_ALL', bool, True)
MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

REG_VERIFY_URL = 'http://127.0.0.1:3000/account/{}/verify-email/{}/'
REG_SITE_NAME = _('Название сайта')

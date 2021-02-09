from .common import *  # noqa
from apps.settings.common import env
from django.utils.translation import gettext_lazy as _

EMAIL_CONFIG = env.email(default='smtp://no-reply@:<password>@postfix:25')
DEFAULT_FROM_EMAIL = 'no-reply@example.com'
SERVER_EMAIL = EMAIL_CONFIG.get('EMAIL_HOST_USER', 'no-reply@example.com')
vars().update(EMAIL_CONFIG)

CACHES = {
    'default': env.cache(default='redis://redis:6379/0'),
    'session': env.cache(default='redis://redis:6379/1'),
}

REG_VERIFY_URL = 'http://127.0.0.1:3000/account/{}/verify-email/{}/'
REG_SITE_NAME = _('Название сайта')

#BROKER_URL = os.environ.get(env.DEFAULT_CACHE_ENV, 'amqp://guest:guest@127.0.0.1:5672//')
#CELERY_RESULT_BACKEND = os.environ.get(env.DEFAULT_CACHE_ENV, 'amqp://guest:guest@127.0.0.1:5672//')

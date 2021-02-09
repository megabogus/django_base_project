from .common import *  # noqa

SECRET_KEY = 'not-a-valid-secret-key'
DATABASES = {
    'default': env.db(default='postgres://django:django@127.0.0.1:5432/django'),
}
CACHES = {
    'default': env.cache(default='redis://127.0.0.1:6379/0'),
    'session': env.cache(default='redis://127.0.0.1:6379/1'),
}

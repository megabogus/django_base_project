import os
from apps.settings.common import env


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME', 'app_db'),
        'USER': os.environ.get('DB_USER', 'app'),
        'PASSWORD': os.environ.get('DB_PASS', 'secret'),
        'HOST': os.environ.get('DB_HOST', 'db'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

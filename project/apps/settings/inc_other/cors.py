from apps.settings.common import env

# https://github.com/ottoyiu/django-cors-headers
CORS_ORIGIN_ALLOW_ALL = env('CORS_ORIGIN_ALLOW_ALL', bool, False)
CORS_ORIGIN_WHITELIST = env('CORS_ORIGIN_WHITELIST', list, [])

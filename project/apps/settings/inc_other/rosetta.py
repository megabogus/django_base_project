from apps.settings.common import env

# https://github.com/mbi/django-rosetta
ROSETTA_MESSAGES_PER_PAGE = env('ROSETTA_MESSAGES_PER_PAGE', int, 50)
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = False
ROSETTA_WSGI_AUTO_RELOAD = True
ROSETTA_UWSGI_AUTO_RELOAD = True

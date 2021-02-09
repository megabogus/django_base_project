from apps.settings.common import env


EMAIL_CONFIG = env.email(default='smtp://mailcatcher')
DEFAULT_FROM_EMAIL = 'no-reply@example.com'
SERVER_EMAIL = EMAIL_CONFIG.get('EMAIL_HOST_USER', 'no-reply@example.com')
vars().update(EMAIL_CONFIG)

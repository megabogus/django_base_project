# AUTHENTICATION_BACKENDS
AUTH_USER_MODEL = 'accounts.User'
# LOGIN_REDIRECT_URL
LOGIN_URL = '/admin/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
# LOGOUT_REDIRECT_URL
# AUTH_PASSWORD_VALIDATORS

MIN_PASSWORD_LENGTH = 12

# Backends
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
    'oauth2_provider.backends.OAuth2Backend',
)

OAUTH2_PROVIDER = {
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups', '*': 'all action'},
    'OAUTH2_BACKEND_CLASS': 'oauth2_provider.oauth2_backends.JSONOAuthLibCore',
}

import settings

API_URL = getattr(settings, 'API_URL', 'go.vumi.org/api/v1/go')
AUTH_TOKEN = getattr(settings, 'AUTH_TOKEN', None)

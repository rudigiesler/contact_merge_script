import settings

API_URL = getattr(settings, 'API_URL', 'go.vumi.org/api/v1/go')
AUTH_TOKEN = getattr(settings, 'AUTH_TOKEN', None)
FIELDS = getattr(settings, 'FIELDS', [
    'name', 'surname', 'email_address', 'dob', 'created_at', 'twitter_handle',
    'facebook_id', 'bbm_pin', 'gtalk_id', 'mxit_id', 'wechat_id', 'msisdn'])
DICT_FIELDS = getattr(settings, 'DICT_FIELDS', ['extra', 'subscription'])
LIST_FIELDS = getattr(settings, 'LIST_FIELDS', ['groups'])

import settings
import logging

API_URL = getattr(settings, 'API_URL', 'go.vumi.org/api/v1/go')
AUTH_TOKEN = getattr(settings, 'AUTH_TOKEN', None)
FIELDS = getattr(settings, 'FIELDS', [
    'name', 'surname', 'email_address', 'dob', 'created_at', 'twitter_handle',
    'facebook_id', 'bbm_pin', 'gtalk_id', 'mxit_id', 'wechat_id', 'msisdn'])
DICT_FIELDS = getattr(settings, 'DICT_FIELDS', ['extra', 'subscription'])
LIST_FIELDS = getattr(settings, 'LIST_FIELDS', ['groups'])
LOGGING_LEVEL = getattr(settings, 'LOGGING_LEVEL', logging.WARNING)
LOG_FILE = getattr(settings, 'LOG_FILE', 'contact_merge_script.log')
CONTACTS_FILENAME = getattr(settings, 'CONTACTS_FILENAME', 'contacts.json')
PROCESSED_CONTACTS_FILENAME = getattr(
    settings, 'PROCESSED_CONTACTS_FILENAME', 'processed_contacts.json')

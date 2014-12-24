import logging
import json

from go_http.contacts import ContactsApiClient
import app_settings as settings

logging.basicConfig(
    filename=settings.LOG_FILE, level=settings.LOGGING_LEVEL)

DELETE_CONTACTS = False

try:
    api = ContactsApiClient(settings.AUTH_TOKEN, settings.API_URL)
    logging.info('Created API successfully')
except Exception as e:
    logging.error('Error creating API')
    logging.debug('API error: %s' % e.message)
    raise e


def get_keys(items):
    keys = []
    for item in items:
        key = item.get('key', None)
        if key is not None:
            keys.append(key)
    return keys

with open(settings.PROCESSED_CONTACTS_FILENAME, 'r') as processed:
    for item in processed:
        item = json.loads(item)
        old_contacts = item.get('old_contacts')
        old_keys = get_keys(old_contacts)
        # Delete old contacts
        for key in old_keys:
            try:
                api.get_contact(key)
                logging.info('Fetched contact with key %s' % key)
                logging.debug('Contact: %s')
            except Exception as e:
                logging.error('Error fetching contact')
                logging.debug('Contact key: %s' % key)
                logging.debug('Error: %s' % e.message)
                continue
            try:
                if DELETE_CONTACTS:
                    api.delete_contact(key)
            except Exception as e:
                logging.warning('Error deleting contact')
                logging.debug('Contact key: %s' % key)
                logging.debug('Error: %s' % e.message)

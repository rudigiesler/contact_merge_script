from collections import defaultdict
import logging

import app_settings as settings
from go_http.contacts import ContactsApiClient

logging.basicConfig(
    filename=settings.LOG_FILE, level=settings.LOGGING_LEVEL)

try:
    api = ContactsApiClient(settings.AUTH_TOKEN, settings.API_URL)
    logging.info('Created API successfully')
except Exception as e:
    logging.error('Error creating API')
    logging.debug('API error: %s' % e.message)
    raise e

grouped_contacts = defaultdict(list)

for contact in api.contacts():
    try:
        msisdn = contact['msisdn']
        grouped_contacts[msisdn].append(contact)
        logging.info('Fetched contact with msisdn %s' % msisdn)
    except Exception as e:
        logging.warning('Error in getting contact')
        logging.debug('Error: %s' % e.message)
        logging.debug('Contact: %s' % contact)


def get_first_value(items, key):
    for item in items:
        value = item.get(key, None)
        if value is not None:
            return value


def combine_dictionary_values(items, key):
    result = {}
    for item in items:
        result.update(item.get(key, {}))
    return result


def combine_set_values(items, key):
    result = set(item.get(key, None) for item in items)
    result.discard(None)
    return list(result)


def get_keys(items):
    keys = []
    for item in items:
        key = item.get('key', None)
        if key is not None:
            keys.append(key)
    return keys

for msisdn, contacts in grouped_contacts.iteritems():
    if len(contacts) <= 1:
        continue

    new_contact = {}
    old_keys = []
    try:
        for field in settings.FIELDS:
            new_contact[field] = get_first_value(contacts, field)
        for field in settings.DICT_FIELDS:
            new_contact[field] = combine_dictionary_values(contacts, field)
        for field in settings.LIST_FIELDS:
            new_contact[field] = combine_set_values(contacts, field)
        old_keys = get_keys(contacts)
        logging.info('Processed contact with MSISDN %s' % msisdn)
    except Exception as e:
        logging.error('Error processing contacts')
        logging.debug('Contacts: %s' % contacts)
        logging.debug('Error: %s' % e.message)
        continue  # Don't create new contact
    # Create new contact
    try:
        api.create_contact(new_contact)
        logging.info('Created contact with msisdn %s', new_contact['msisdn'])
    except Exception as e:
        logging.error('Error creating new contact')
        logging.debug('Contact: %s' % new_contact)
        logging.debug('Error: %s' % e.message)
        continue  # Don't delete the contacts
    # Delete old contacts
    for key in old_keys:
        try:
            api.delete_contact(key)
            logging.info('Deleted contact with key %s' % key)
        except Exception as e:
            logging.warning('Error deleting contact')
            logging.debug('Contact key: %s' % key)
            logging.debug('Error: %s' % e.message)

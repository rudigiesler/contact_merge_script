from collections import defaultdict
import logging
import json

import app_settings as settings

logging.basicConfig(
    filename=settings.LOG_FILE, level=settings.LOGGING_LEVEL)

grouped_contacts = defaultdict(list)

with open(settings.CONTACTS_FILENAME) as contacts:
    for contact in contacts:
        contact = json.loads(contact)
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
    result = set()
    for item in items:
        result |= set(item.get(key, []))
    result.discard(None)
    return list(result)


def get_keys(items):
    keys = []
    for item in items:
        key = item.get('key', None)
        if key is not None:
            keys.append(key)
    return keys

processed_contacts = open(settings.PROCESSED_CONTACTS_FILENAME, 'w')
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
    # Save new contacts
    result = {'old_contacts': contacts, 'new_contact': new_contact}
    processed_contacts.write(json.dumps(result))

processed_contacts.close()

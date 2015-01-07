import argparse
import logging
import json

from go_http.contacts import ContactsApiClient
import app_settings as settings

logging.basicConfig(
    filename=settings.LOG_FILE, level=settings.LOGGING_LEVEL)

parser = argparse.ArgumentParser(description="Upload contacts")
parser.add_argument(
    'filename', metavar='filename', type=str, nargs=1,
    help='Filename to find the duplicate contact results.')
args = parser.parse_args()


def get_keys(items):
    keys = []
    for item in items:
        key = item.get('key', None)
        if key is not None:
            keys.append(key)
    return keys

try:
    api = ContactsApiClient(settings.AUTH_TOKEN, settings.API_URL)
    logging.info('Created API successfully')
except Exception as e:
    logging.error('Error creating API')
    logging.debug('API error: %s' % e.message)
    raise e

with open(args.filename[0], 'r') as processed:
    for item in processed:
        item = json.loads(item)
        new_contact = item.get('new_contact')
        old_contacts = item.get('old_contacts')
        old_keys = get_keys(old_contacts)
        try:
            api.create_contact(new_contact)
            logging.info(
                'Created contact with msisdn %s', new_contact['msisdn'])
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

print('Uploaded changes from %s' % args.filename[0])

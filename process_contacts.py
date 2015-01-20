import argparse
from collections import defaultdict
import logging
import json

import app_settings as settings

logging.basicConfig(
    filename=settings.LOG_FILE, level=settings.LOGGING_LEVEL)

parser = argparse.ArgumentParser(description="Deduplicate contacts")
parser.add_argument(
    'contacts_filename', type=str, nargs=1,
    help='Filename to find the duplicate contacts.')
parser.add_argument(
    'results_filename', type=str, nargs=1,
    help='Filename to store the results of the duplicate contacts.')
parser.add_argument(
    '--append', '-a', dest='file_mode', default='w', action='store_const',
    const='a', help='Append processed contacts to the file instead of the' +
    ' default overwrite')
parser.add_argument(
    '--merge-on', '-m', type=str, dest='merge_field', default='msisdn',
    help='Contact field used to detect duplicate contacts')
args = parser.parse_args()

grouped_contacts = defaultdict(list)
contact_count = 0
merge_field = args.merge_field

with open(args.contacts_filename[0]) as contacts:
    for contact in contacts:
        contact_count += 1
        contact = json.loads(contact)
        try:
            group_key = contact[merge_field]
            grouped_contacts[group_key].append(contact)
            logging.info(
                'Fetched contact with %s %s' % (merge_field, group_key))
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

processed_contacts = open(args.results_filename[0], args.file_mode)
for group_key, contacts in grouped_contacts.iteritems():
    if len(contacts) <= 1:
        continue

    new_contact = {}
    old_keys = []
    try:
        contacts.sort(key=lambda c: c.get('created_at'))
        for field in settings.FIELDS:
            new_contact[field] = get_first_value(contacts, field)
        for field in settings.DICT_FIELDS:
            new_contact[field] = combine_dictionary_values(contacts, field)
        for field in settings.LIST_FIELDS:
            new_contact[field] = combine_set_values(contacts, field)
        logging.info('Processed contact with %s %s' % (merge_field, group_key))
    except Exception as e:
        logging.error('Error processing contacts')
        logging.debug('Contacts: %s' % contacts)
        logging.debug('Error: %s' % e.message)
        continue  # Don't create new contact
    # Save new contacts
    result = {'old_contacts': contacts, 'new_contact': new_contact}
    processed_contacts.write(json.dumps(result))
    processed_contacts.write('\n')

processed_contacts.close()

print('Total contacts: %d' % contact_count)
print('Unique contacts: %d' % len(grouped_contacts))
print('Number of contacts per unique contact: %f' % (
    1.0 * contact_count / len(grouped_contacts)))
print('Stored duplicate contact results from %s in %s' % (
    args.contacts_filename[0], args.results_filename[0]))

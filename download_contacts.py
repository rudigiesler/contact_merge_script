import argparse
import logging
import json

from go_http.contacts import ContactsApiClient
import app_settings as settings

logging.basicConfig(
    filename=settings.LOG_FILE, level=settings.LOGGING_LEVEL)

parser = argparse.ArgumentParser(description="Download contacts")
parser.add_argument(
    'filename', type=str, nargs=1,
    help='Filename to store the downloaded contacts in.')
parser.add_argument(
    '--append', '-a', dest='file_mode', default='w', action='store_const',
    const='a', help='Append downloaded contacts to the file instead of the' +
    ' default overwrite')
args = parser.parse_args()

try:
    api = ContactsApiClient(settings.AUTH_TOKEN, settings.API_URL)
    logging.info('Created API successfully')
except Exception as e:
    logging.error('Error creating API')
    logging.debug('API error: %s' % e.message)
    raise e

f = None
try:
    f = open(args.filename[0], args.file_mode)
except Exception as e:
    logging.error('Error creating file')
    logging.debug('File error: %s' % e.message)
    raise e

for contact in api.contacts():
    try:
        f.write(json.dumps(contact))
        f.write('\n')
    except Exception as e:
        logging.warning('Error in getting contact')
        logging.debug('Error: %s' % e.message)
        logging.debug('Contact: %s' % contact)
f.close()

print 'Contacts downloaded to %s' % args.filename[0]

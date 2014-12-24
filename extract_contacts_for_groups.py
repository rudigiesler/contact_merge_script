import json

INFILE = 'contacts.json'
OUTFILE = 'filtered_contacts.json'

GROUPS = []

outf = open(OUTFILE, 'w')

with open(INFILE, 'r') as inf:
    for contact in inf:
        contact_groups = json.loads(contact).get('groups')
        for group in GROUPS:
            if group in contact_groups:
                outf.write(contact)
                continue

outf.close()

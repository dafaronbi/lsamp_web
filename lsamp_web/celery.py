from __future__ import absolute_import,unicode_literals
import os
import requests
from celery import Celery
from django.conf import settings
from collections import Counter

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lsamp_web.settings')

app = Celery('lsamp_web')
app.conf.enable_utc = False

app.conf.update(timezone = "America/New_York")

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # update database every hour.
    sender.add_periodic_task(3600, download_data.s(), name='update-data-base')


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(settings, namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

@app.task(bind=True)
def download_data(self):
    #get all sheet values
    smartsheet = requests.get("https://api.smartsheet.com/2.0/sheets/976201423579012", headers={'Authorization': 'Bearer R3xflmbloIqxFh6JfBfjWgT01RB2Sx5AOCewZ'})

    #count number of occurences of name
    count = Counter()

    for person in smartsheet.json()['rows']:

        #get row id
        id = person['id']

        #get name
        name = person['cells'][2]['value'].lower() + " " + person['cells'][3]['value'].lower()
        count.update([name])

        #get attachment stored in row
        row_attachment = requests.get("https://api.smartsheet.com/2.0/sheets/976201423579012/rows/" + str(id) + "/attachments",headers={'Authorization': 'Bearer R3xflmbloIqxFh6JfBfjWgT01RB2Sx5AOCewZ'})
        if row_attachment.status_code == 200 and row_attachment.json()['data']:
            attachment_id = row_attachment.json()['data'][0]['id']
            download_url = requests.get("https://api.smartsheet.com/2.0/sheets/976201423579012/attachments/" + str(attachment_id),headers={'Authorization': 'Bearer R3xflmbloIqxFh6JfBfjWgT01RB2Sx5AOCewZ'}).json()['url']
            r = requests.get(download_url, allow_redirects=True)
            open('media/' + name + str(count[name]) + '.jpg', 'wb').write(r.content)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
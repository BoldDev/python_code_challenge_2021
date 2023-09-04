from __future__ import absolute_import, unicode_literals
from celery import Celery
from django.conf import settings

import os
import dotenv
dotenv.load_dotenv()

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_challenge.settings')

app = Celery('python_challenge')

app.conf.update(
    accept_content=['application/json'],
    task_serializer='json',
    result_serializer='json',
    enable_utc=True,
    timezone='UTC',
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    broker_url=os.environ.get('CELERY_BROKER_URL'),
    result_backend=os.environ.get('CELERY_BROKER_URL'),
)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(settings, namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

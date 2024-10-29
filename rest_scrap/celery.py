from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set Django settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest_scrap.settings')
app = Celery('rest_scrap')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
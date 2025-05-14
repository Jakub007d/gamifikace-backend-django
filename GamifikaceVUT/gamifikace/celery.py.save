import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamifikace.settings')

app = Celery('gamifikace')
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'django-db'
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
print("🚨 CELERY CONFIG FROM SETTINGS:")
print("BROKER:", app.conf.broker_url)
print("RESULT BACKEND:", app.conf.result_backend)

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao_eventos.settings')
app = Celery('gestao_eventos')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
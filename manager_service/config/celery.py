import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'daily_pay_task': {
        'task': 'tasks.create_daily_bills',
        'schedule': crontab(minute=0, hour=12)
    },
}

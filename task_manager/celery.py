from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

app = Celery('task_manager')

# Utilise le fichier settings.py pour la configuration
app.config_from_object('django.conf:settings', namespace='CELERY')

# Trouve les tâches définies dans installed apps
app.autodiscover_tasks()



app.conf.beat_schedule = {
    'send-reminders-every-minute': {
        'task': 'your_app.tasks.send_reminders',
        'schedule': crontab(minute='*/1'),  # Vérifie toutes les minutes
    },
}


from celery import shared_task
from django.utils import timezone  # Import de timezone
from tasks.models import Task

@shared_task
def send_task_reminders():
    tasks = Task.objects.filter(reminder__lte=timezone.now(), completed=False)
    for task in tasks:
        task.send_reminder()


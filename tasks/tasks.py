from celery import shared_task
from .models import Task
from .utils import send_task_reminder
from datetime import datetime

@shared_task
def send_reminders():
    now = datetime.now()
    tasks = Task.objects.filter(reminder__lte=now, completed=False)
    for task in tasks:
        send_task_reminder(task)


from django.db import models
from django.utils import timezone
from .utils import send_sms  # Assure-toi d'importer la fonction

from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    reminder = models.DateTimeField(null=True, blank=True)  # Champ pour le rappel
    completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')
    assigned_to = models.ForeignKey(User, related_name='tasks', on_delete=models.SET_NULL, null=True, blank=True)  # Utilisateur assigné
    comments = models.ManyToManyField('Comment', related_name='task_comments', blank=True)  # Commentaires

    def __str__(self):
        return self.title

class Comment(models.Model):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.task}"

    def send_reminder(self):
        if self.reminder and timezone.now() >= self.reminder:
            message = f"Rappel : La tâche '{self.title}' est prévue pour {self.due_date}."
            send_sms(self.phone_number, message)

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('User', 'User'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='User')
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True) 
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)

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
    assigned_to = models.ForeignKey(CustomUser, related_name='tasks', on_delete=models.SET_NULL, null=True, blank=True)  # Utilisateur assigné
    comments = models.ManyToManyField('Comment', related_name='task_comments', blank=True)  # Commentaires

    def __str__(self):
        return self.title

class Comment(models.Model):
    task = models.ForeignKey(Task, related_name='task_comments', on_delete=models.CASCADE)  # Utiliser 'task_comments' pour éviter le conflit
    author = models.ForeignKey(CustomUser, related_name='user_comments', on_delete=models.CASCADE)  # Utiliser 'user_comments' pour éviter le conflit
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.task}"

from twilio.rest import Client
from django.conf import settings

def send_sms(to, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=to
    )

# Mettre à jour le modèle d'utilisateur personnalisé dans settings.py
AUTH_USER_MODEL = 'tasks.CustomUser'

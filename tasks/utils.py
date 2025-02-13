from django.core.mail import send_mail
from django.conf import settings

def send_task_reminder(task):
    subject = f"Rappel pour votre tâche : {task.title}"
    message = f"Ceci est un rappel pour votre tâche : {task.title}\n\nDescription : {task.description}\nDate d'échéance : {task.due_date}\nPriorité : {task.get_priority_display()}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['recipient@example.com']  # Remplacer par l'email de l'utilisateur
    send_mail(subject, message, email_from, recipient_list)

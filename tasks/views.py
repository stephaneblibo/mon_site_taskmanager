from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, CustomUser
from .forms import TaskForm
from rest_framework import generics
from .serializers import TaskSerializer
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q
from django.core.mail import send_mail
from django.views.generic import ListView
from .mixins import AdminRequiredMixin  # Importez depuis mixins.py

def is_admin(user):
    return user.is_authenticated and isinstance(user, CustomUser) and user.role == 'Admin'

@login_required
def task_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        tasks = Task.objects.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
    else:
        tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def home(request):
    return render(request, 'tasks/home.html')


from .models import Task, Comment
from .forms import TaskForm, CommentForm

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
            return redirect('task_detail', pk=task.pk)
    else:
        comment_form = CommentForm()
    return render(request, 'tasks/task_detail.html', {'task': task, 'comment_form': comment_form})



def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            send_mail(
                'Nouvelle tâche créée',
                f'Tâche "{task.title}" a été créée.',
                'kaderblibo4@gmail.com',  # Remplacez par une adresse email valide
                ['kaderblibo4@gmail.com'],  # Remplacez par une adresse email valide
                fail_silently=False,
            )
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

class TaskListCreateAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

def task_statistics(request):
    priority_counts = Task.objects.values('priority').annotate(total=Count('priority')).order_by('priority')
    return render(request, 'tasks/task_statistics.html', {'priority_counts': priority_counts})

class TaskListView(AdminRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'


from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()
                # Créer un profil utilisateur associé si nécessaire
                # profile = Profile.objects.create(user=user)
                return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})



from .forms import TaskForm

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_edit.html', {'form': form})


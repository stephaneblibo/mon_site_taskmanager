from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Task

class TaskModelTest(TestCase):

    def test_task_creation(self):
        task = Task.objects.create(title="Test Task")
        self.assertEqual(task.title, "Test Task")


# Create your tests here.


class TaskAPITestCase(APITestCase):

    def test_create_task(self):
        url = reverse('task_list_create_api')
        data = {'title': 'Test Task'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'Test Task')

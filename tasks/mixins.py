# tasks/mixins.py
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import CustomUser

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and isinstance(self.request.user, CustomUser) and self.request.user.role == 'Admin'

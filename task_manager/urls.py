from django.contrib import admin
from django.urls import path, include
from tasks.views import home


urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  
    path('accounts/', include('django.contrib.auth.urls')),  # URL de connexion alec. Django auth
    path('tasks/', include('tasks.urls')),
]

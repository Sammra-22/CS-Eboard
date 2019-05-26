"""
cs_manager URL Configuration

"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('eboard/', include('eboard.urls')),
    path('admin/', admin.site.urls),
]

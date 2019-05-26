"""
eboard URL Configuration

"""
from django.urls import path

from eboard import views

urlpatterns = [
    path('', views.index, name='index'),
]

"""
cs_manager URL Configuration

"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import include

urlpatterns = [
    url('eboard/(?P<slug>[\w-]+)/', include('eboard.urls')),
    url('admin/', admin.site.urls),
]

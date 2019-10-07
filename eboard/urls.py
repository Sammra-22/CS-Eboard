"""
eboard URL Configuration

"""
from django.conf.urls import url
from django.urls import path

from eboard import views
from eboard.views import OrganizationDashboardView, OrganizationLoginView, OrganizationLogoutView, ClientCreateView

app_name = 'dashboard'
urlpatterns = [
    url(r'^login/$', OrganizationLoginView.as_view(), name='login'),
    url(r'^logout/$', OrganizationLogoutView.as_view(), name='logout'),
    url(r'^add/$', ClientCreateView.as_view(), name='add-client'),
    url(r'^$', OrganizationDashboardView.as_view(), name='index'),
]

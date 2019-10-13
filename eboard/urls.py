"""
eboard URL Configuration

"""
from django.conf.urls import url
from django.urls import include

from eboard.views import OrganizationDashboardView, OrganizationLoginView, OrganizationLogoutView, ClientCreateView, \
    ClientListView, ScheduleCalendarView

app_name = 'dashboard'
urlpatterns = [
    url(r'^login/$', OrganizationLoginView.as_view(), name='login'),
    url(r'^logout/$', OrganizationLogoutView.as_view(), name='logout'),
    url(r'^clients/$', ClientListView.as_view(), name='clients-list'),
    url(r'^clients/add$', ClientCreateView.as_view(), name='client-add'),
    url(r'^schedule/$', ScheduleCalendarView.as_view(), name='schedule'),
    url(r'^$', OrganizationDashboardView.as_view(), name='index'),
]

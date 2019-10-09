"""
eboard URL Configuration

"""
from django.conf.urls import url
from eboard.views import OrganizationDashboardView, OrganizationLoginView, OrganizationLogoutView, ClientCreateView, \
    ClientListView

app_name = 'dashboard'
urlpatterns = [
    url(r'^login/$', OrganizationLoginView.as_view(), name='login'),
    url(r'^logout/$', OrganizationLogoutView.as_view(), name='logout'),
    url(r'^clients/$', ClientListView.as_view(), name='clients-list'),
    url(r'^clients/add$', ClientCreateView.as_view(), name='client-add'),
    url(r'^$', OrganizationDashboardView.as_view(), name='index'),
]

import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import ModelFormMixin, CreateView, FormMixin
from django.utils.translation import gettext_lazy as _
from schedule.periods import Period, Year
from schedule.views import CalendarByPeriodsView

from eboard.clients.models import Client
from eboard.forms import ClientForm, ClientSearchForm
from eboard.organizations.models import Organization
from eboard.utils import filter_client_queryset


def index(request):
    return HttpResponse("Hello, world. You're at the eboard index.")


class OrganizationContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        context['slug'] = slug
        context['organization'] = get_object_or_404(Organization, slug=slug)
        return context


class OrganizationPermissionMixin(
        LoginRequiredMixin,
        PermissionRequiredMixin,
        OrganizationContextMixin,
):
    permission_required = 'editor'

    def get_permission_object(self):
        slug = self.kwargs.get('slug', None)
        return get_object_or_404(Organization, slug=slug)

    def get_login_url(self):
        slug = self.kwargs.get('slug', None)
        return reverse('dashboard:login', args=[slug])


class ClientFormMixin(
    OrganizationPermissionMixin,
    ModelFormMixin,
):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'org': self.get_permission_object(),
        })
        return kwargs

class OrganizationLoginView(OrganizationContextMixin, LoginView):
    template_name = 'pages/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        slug = self.kwargs['slug']
        return reverse('dashboard:index', args=[slug])

    def form_valid(self, form):
        user = form.get_user()
        slug = self.kwargs['slug']
        organization = get_object_or_404(Organization, slug=slug)
        if user.has_perm('editor', organization):
            return super().form_valid(form)
        data = {'username': form.username_field.verbose_name}
        form.add_error(None, form.error_messages['invalid_login'] % data)
        return super().form_invalid(form)


class OrganizationLogoutView(LogoutView):
    def get_next_page(self):
        slug = self.kwargs.get('slug', None)
        return reverse('dashboard:login', args=[slug])


class OrganizationDashboardView(OrganizationPermissionMixin,
                                TemplateView):
    template_name = 'pages/index.html'


class ClientCreateView(ClientFormMixin, SuccessMessageMixin, CreateView):
    template_name = 'pages/client-new.html'
    model = Client
    form_class = ClientForm
    success_message = _('The client was created successfully')

    def get_initial(self):
        return {
            'first_name': self.request.POST.get('first_name', ''),
            'last_name': self.request.POST.get('last_name', ''),
            'gender': self.request.POST.get('gender', ''),
            'birth_date': self.request.POST.get('birth_date', ''),
            'email': self.request.POST.get('email', ''),
            'phone': self.request.POST.get('phone', ''),
        }

    def get_success_url(self):
        slug = self.kwargs['slug']
        return reverse(
            'dashboard:index', args=[
                slug,
            ]
        )


class ClientListView(OrganizationPermissionMixin, ListView, FormMixin):
    template_name = 'pages/clients.html'
    model = Client
    paginate_by = 12
    form_class = ClientSearchForm

    def get_initial(self):
        return {'search': self.request.GET.get('search', '')}

    def get_queryset(self):
        search_query = self.request.GET.get('search', None)
        organization = self.get_permission_object()
        queryset = Client.objects.filter(organization=organization, )
        if search_query:
            return filter_client_queryset(queryset, search_query)
        return queryset


class ScheduleCalendarView(OrganizationPermissionMixin, CalendarByPeriodsView):
    template_name = "pages/schedule.html"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        today = datetime.datetime.now()
        this_week = Period(None, today, today + datetime.timedelta(days=7))
        self.kwargs['period'] = Year
        return super().get_context_data(**kwargs)

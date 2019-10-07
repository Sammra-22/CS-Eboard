from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import ModelFormMixin, CreateView
from django.utils.translation import gettext_lazy as _

from eboard.clients.models import Client
from eboard.forms import ClientForm
from eboard.organizations.models import Organization


def index(request):
    return HttpResponse("Hello, world. You're at the eboard index.")


class OrganizationContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        context['slug'] = slug
        context['organization'] = get_object_or_404(Organization, slug=slug)
        return context


class OrganizationPermissionRequiredMixin(
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
    OrganizationPermissionRequiredMixin,
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


class OrganizationDashboardView(OrganizationPermissionRequiredMixin,
                                TemplateView):
    template_name = 'pages/index.html'


class ClientCreateView(ClientFormMixin, SuccessMessageMixin, CreateView):
    template_name = 'pages/client-add.html'
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

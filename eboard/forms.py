from django import forms

from eboard.clients.models import Client
from django.utils.translation import gettext_lazy as _


class ClientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop('org')
        super().__init__(*args, **kwargs)

    def save(self, **kwargs):
        instance = super().save(commit=False)
        instance.organization = self.organization
        instance.save(kwargs)

    class Meta:
        model = Client
        fields = (
            'first_name',
            'last_name',
            'gender',
            'birth_date',
            'email',
            'phone',
        )
        labels = {
            'first_name': _('First name'),
            'last_name': _('Last name'),
            'gender': _('Gender'),
            'birth_date': _('Birth date'),
            'email': _('Email'),
            'phone': _('Phone number'),
        }

class ClientSearchForm(forms.Form):
    search = forms.CharField(required=False)

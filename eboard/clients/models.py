from django.db import models
from model_utils import Choices

from eboard.mixins import UpdateModelMixin
from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from eboard.organizations.models import Organization

GENDER_MALE = 'male'
GENDER_FEMALE = 'female'
GENDER = Choices(
    (GENDER_MALE, _('Male')),
    (GENDER_FEMALE, _('Female')),
)


class Client(
        UpdateModelMixin,
        TimeStampedModel,
):
    organization = models.ForeignKey(
        Organization,
        related_name='clients',
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(
        _('first name'),
        max_length=30,
        blank=False,
    )
    last_name = models.CharField(
        _('last name'),
        max_length=30,
        blank=False,
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER,
    )
    birth_date = models.DateField(
        _('birth date'),
        max_length=8,
    )
    email = models.EmailField(
        _('email address'),
        max_length=255,
        blank=True,
    )
    phone = PhoneNumberField(
        _('phone number'),
        blank=True,
    )

    def get_full_name(self):
        return '{first_name} {last_name}'.format(
            first_name=self.first_name,
            last_name=self.last_name,
        )

    def update(self, **kwargs):
        self.allowed_attributes = {
            'first_name', 'last_name', 'gender', 'birth_date', 'email', 'phone'
        }
        return super().update(**kwargs)

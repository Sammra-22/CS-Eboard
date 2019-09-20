from django.db import models
from django_extensions.db.fields import AutoSlugField

from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _


class OrganizationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class Organization(TimeStampedModel):
    objects = OrganizationManager()
    name = models.CharField(
        _('name'),
        max_length=30,
        unique=True,
    )
    slug = AutoSlugField(
        populate_from='name',
        unique=True,
    )
    active = models.BooleanField(
        _('active'),
        default=True,
    )

    def clean(self):
        self.name = self.name.capitalize()

    def __str__(self):
        return 'Org [#{pk}] - {name}'.format(
            pk=self.pk,
            name=self.name,
        )

from django.contrib import admin


from eboard.organizations.models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Organization._meta.fields]

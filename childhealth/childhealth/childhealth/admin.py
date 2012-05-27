from childhealth.models import Country, Organization, Patient
from django.contrib import admin

class PatientAdmin(admin.ModelAdmin):
    exclude = ('short_string',)

admin.site.register(Country)
admin.site.register(Organization)
admin.site.register(Patient, PatientAdmin)

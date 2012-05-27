from childhealth.models import Country, Organization, Patient, Visit
from django.contrib import admin

class VisitInline(admin.StackedInline):
    model = Visit

class PatientAdmin(admin.ModelAdmin):
    exclude = ('short_string',)
    inlines = [VisitInline]

admin.site.register(Country)
admin.site.register(Organization)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Visit)

import logging

from childhealth.models import Country, Organization, Patient, Visit
from django.contrib import admin

class VisitInline(admin.StackedInline):
    model = Visit

class PatientAdmin(admin.ModelAdmin):
    exclude = ('short_string',)
    inlines = [VisitInline]

    # Add request.user to patient
    # See http://stackoverflow.com/a/2992150/34935
    def save_model(self, request, obj, form, change):
        logging.info("request %s obj %s form %s change %s"
                     % (request, obj, form, change))
        if getattr(obj, 'created_by_user', None) is None:
            obj.created_by_user = request.user
        obj.edited_by_user = request.user
        obj.save()

admin.site.register(Country)
admin.site.register(Organization)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Visit)

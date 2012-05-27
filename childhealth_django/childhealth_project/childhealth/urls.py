from django.conf.urls import patterns, include, url
from django.views.generic import ListView
from childhealth.models import Patient

# Enable admin
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'childhealth.views.home', name='home'),
    # url(r'^childhealth/', include('childhealth.childhealth.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

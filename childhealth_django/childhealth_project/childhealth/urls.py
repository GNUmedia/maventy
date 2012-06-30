from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from childhealth.models import Patient

# Enable admin
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'childhealth.views.home', name='home'),
    # url(r'^childhealth/', include('childhealth.childhealth.urls')),

    url(r'^patients/$',
        ListView.as_view(
            model = Patient)),
#            queryset=Patient.objects.order_by('-created_date')[:5],
#            context_object_name='latest_patient_list',
#            template_name='patient/index.html')),
    url(r'^patient/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Patient,
            template_name='patient/detail.html')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

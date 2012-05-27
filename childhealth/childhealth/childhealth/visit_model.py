from django.db import models

from patient_model import Patient

from datetime import date

class Visit(models.Model):
    STANDING = 1
    RECUMBENT = 2
    HEIGHT_POSITION = (
        (STANDING, 'Standing'),
        (RECUMBENT, 'Recumbent'))

    patient = models.ForeignKey(Patient)

    # Date created in this DB
    created_date = models.DateTimeField(auto_now_add=True)
    # Last edited in this DB
    last_edited = models.DateTimeField(auto_now=True)

    # user who created the visit
#    created_by_user = models.ReferenceProperty(blank=True, null=True)

    evaluator_name = models.CharField(blank=True, max_length=255)

  # TODO(dan): Make visit_number blank=False.  It's a little tricky.
#  visit_number = models.IntegerProperty(blank=True, null=True)

    # Unfortunately, due to the way we init visit with parent Patient,
    # we need to specify a default visit_date.  On the bright side,
    # form validation can still catch an unset property
    visit_date = models.DateField(default = date.today())
    weight = models.FloatField(default = 0.0)
    head_circumference = models.FloatField(blank=True, null=True)
    height = models.FloatField(default = 0.0)
    # Unfortunately, due to the way we init visit with parent Patient,
    # we need to specify a default height_position.  On the bright side,
    # form validation can still catch an unset property
    height_position = models.IntegerField(choices=HEIGHT_POSITION,
                                          default=STANDING)
#    visit_statistics = models.ReferenceProperty(
#        reference_class = VisitStatistics,
#        blank=True, null=True, default = None)

    # 'organization' comes from the parent Patient
    # We duplicate it on Visit in order to query against it
    # TODO(dan): Change to blank=False
    # organization = models.CharField(blank=True)

    # Notes about the visit
    # TODO(dan): Internationalize verbose_name
    notes = models.TextField(blank=True) #, verbose_name = _('Visit notes'))

    def __unicode__(self):
        return ("<id=%s, patient=%s, created_date=%s, last_edited=%s>"
                % (
                self.id,
                self.patient,
                self.created_date.date(),
                self.last_edited.date()))

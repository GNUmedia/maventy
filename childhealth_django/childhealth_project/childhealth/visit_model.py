from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

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

    # weight in kilograms
    # min_value is INPUT_MINWEIGHT from WHO's AnthroComputation.cs
    # max_value is INPUT_MAXWEIGHT from WHO's AnthroComputation.cs
    weight = models.FloatField(
        validators = [MinValueValidator(0.9), MaxValueValidator(58)])

    # head circumference in centimeters
    # (only provide for children 0-24 months old)
    # min_value is INPUT_MINHC from WHO's AnthroComputation.cs
    # max_value is INPUT_MAXHC from WHO's AnthroComputation.cs
    head_circumference = models.FloatField(blank=True, null=True,
                                           validators = [MinValueValidator(25),
                                                         MaxValueValidator(64)])
    # height in centimeters
    # min_value is INPUT_MINLENGTHORHEIGHT from WHO's AnthroComputation.cs
    # max_value is INPUT_MAXLENGTHORHEIGHT from WHO's AnthroComputation.cs
    height = models.FloatField(validators = [MinValueValidator(38),
                                             MaxValueValidator(150)])

    height_position = models.IntegerField(choices=HEIGHT_POSITION)

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

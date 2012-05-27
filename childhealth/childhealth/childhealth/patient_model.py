# -*- coding: utf-8 -*-

from django.db import models

import logging
import util

import misc_models

class Patient(models.Model):
    MALE = 'MALE'
    FEMALE = 'FEMALE'

    # HACK(dan): BELOW_LOWEST_ZSCORE indicates any zscore below -3.
    BELOW_LOWEST_ZSCORE = -4.0

    # Date created in this DB
    created_date = models.DateTimeField(auto_now_add=True)
    # Last edited in this DB
    last_edited = models.DateTimeField(auto_now=True)

    # user who created the visit
    # TODO(dan): Implement custom user
    # created_by_user = models.ForeignKey('User')

    # Easy way to refer to a patient
    short_string = models.CharField(max_length=10, blank=True, unique=True)

    name = models.CharField(max_length=255)
    sex = models.CharField(max_length=10, choices = [(MALE, "Male"),
                                                     (FEMALE, "Female")])
    birth_date = models.DateField()

    residence = models.CharField(max_length=255, blank=True)
    organization = models.ForeignKey('Organization')

    # TODO(dan): How to properly translate country names?  Do we need to?
    country = models.ForeignKey('Country')
    caregiver_name = models.CharField(max_length=255, blank=True)

    # Cached from latest visit, to sort by
  #  latest_visit_date = models.DateField(blank=True, null=True)
    # Cached from latest visit, to sort by
  #  latest_visit = models.ForeignKey('Visit', blank=True, null=True)
  #  latest_visit_number = models.IntegerProperty(blank=True, null=True)
    # Cached from latest_visit_worst_zscore, to filter by
  #  latest_visit_worst_zscore_rounded = models.FloatProperty(blank=True, null=True)

    # Vaccination records
    # TODO(dan): Could do a list property of vaccinations instead.
    # Might be cleaner.

    # polio
  #  polio_vaccinations = VaccinationProperty(blank=True, null=True)

    # diphtérie, Tétanos, Coqueluche (French: diphtheria, tetanus, and whooping cough)
  #  dtc_vaccinations = VaccinationProperty(blank=True, null=True)

    # hepatitis
  #  hepb_vaccinations = VaccinationProperty(blank=True, null=True)

  #  measles_vaccinations = VaccinationProperty(blank=True, null=True)

    # hib is hemophilus influenzae
  #  hib_vaccinations = VaccinationProperty(blank=True, null=True)

    # http://en.wikipedia.org/wiki/Bacillus_Calmette-Gu%C3%A9rin against tuberculosis
  #  bcg_vaccinations = VaccinationProperty(blank=True, null=True)

    # vitamin A
  #  vita_vaccinations = VaccinationProperty(blank=True, null=True)

    # deworming: mebendazole
  #  deworming_vaccinations = VaccinationProperty(blank=True, null=True)

    @staticmethod
    def get_by_short_string(short_string):
      return Patient.objects.filter(short_string = short_string)

    def assign_short_string(self): 
      assert (self.short_string is None or not self.short_string,
             "Tried to assign short_string twice: '%s'" % self.short_string)
      while not self.short_string:
        # 1 / (31^6) = 1e-9 is the probability two strings collide
        # in an empty space
        # TODO(dan): This should be in a transaction
        astr = util.random_string(6)
        if not Patient.get_by_short_string(astr):
          self.short_string = astr
          logging.info('assigned short string: %s' % self.short_string)

    def save(self, *args, **kwargs):
      if not self.short_string: self.assign_short_string()
      # TODO(dan): Add created_by_user
      super(Patient, self).save(*args, **kwargs)

    def __unicode__(self):
      return "%s, %s, %s (%s)" % (self.name,
                                  self.sex,
                                  self.birth_date,
                                  self.short_string)

# -*- coding: utf-8 -*-

from django.db import models

import logging
import util

class Vaccination(object):
  """A class to contain records about a Vaccination given to a patient."""
  def __init__(self, date_list = []):
#    logging.info("__init__ date_list %s id %s" % (date_list, id(date_list)))
    # NOTE(dan): self.dates = date_list is a bug!  date_list persists.
    self.dates = []
    self.dates.extend(date_list)

  def add_date(self, date):
    self.dates.append(date)

  def __str__(self):
    """String for debugging"""
    return "dates %s" % (self.dates)

  def __len__(self):
    return len(self.dates)

  def __cmp__(self, other):
    '''Return -1 if self < other, 0 if self == other, 1 if self > other.'''
    if other is None: return 1
    val = len(self.dates) - len(other.dates)
    if not val:
      # lengths are equal, test members
      for idx in range(len(self.dates)):
        date1 = self.dates[idx]
        date2 = other.dates[idx]
        if not date1 and not date2: val = 0
        elif not date1 and date2: val = -1
        elif date1 and not date2: val = 1
        else:
          tdelta = date1 - date2
          val = tdelta.days
        if val: break 
    return val


class Country(models.Model):
    class Meta:
        verbose_name_plural = "countries"

    name = models.CharField(max_length=255)

    def __unicode__(self):
      return self.name

class Organization(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
      return self.name

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
  #  latest_visit_date = models.DateField(blank=True)
    # Cached from latest visit, to sort by
  #  latest_visit = models.ForeignKey('Visit', blank=True)
  #  latest_visit_number = models.IntegerProperty(blank=True)
    # Cached from latest_visit_worst_zscore, to filter by
  #  latest_visit_worst_zscore_rounded = models.FloatProperty(blank=True)

    # Vaccination records
    # TODO(dan): Could do a list property of vaccinations instead.
    # Might be cleaner.

    # polio
  #  polio_vaccinations = VaccinationProperty(blank=True)

    # diphtérie, Tétanos, Coqueluche (French: diphtheria, tetanus, and whooping cough)
  #  dtc_vaccinations = VaccinationProperty(blank=True)

    # hepatitis
  #  hepb_vaccinations = VaccinationProperty(blank=True)

  #  measles_vaccinations = VaccinationProperty(blank=True)

    # hib is hemophilus influenzae
  #  hib_vaccinations = VaccinationProperty(blank=True)

    # http://en.wikipedia.org/wiki/Bacillus_Calmette-Gu%C3%A9rin against tuberculosis
  #  bcg_vaccinations = VaccinationProperty(blank=True)

    # vitamin A
  #  vita_vaccinations = VaccinationProperty(blank=True)

    # deworming: mebendazole
  #  deworming_vaccinations = VaccinationProperty(blank=True)

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

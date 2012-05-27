from django.db import models

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

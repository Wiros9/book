from django.db import models
from lino.api import dd


class PartnerType(dd.Model):
    name = models.CharField("Name", max_length=20)


class Partner(dd.Model):

    class Meta:
        verbose_name = "Partner"
        verbose_name_plural = "Partners"

    type = models.ForeignKey(PartnerType)
    name = models.CharField("Name", max_length=30)


class Person(Partner):
    first_name = models.CharField("First name", max_length=20)
    last_name = models.CharField("Last name", max_length=20)

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "Persons"


class Partners(dd.Table):
    model = Partner
    # no explicit `label` attribute, so take verbose_name_plural from model


class Persons(Partners):
    model = Person
    # no explicit `label` attribute, so take verbose_name_plural from model


class FunnyPersons(Persons):
    label = "Funny persons"


class MyFunnyPersons(FunnyPersons):
    # no explicit `label` attribute, so inherit from parent
    pass


from .dynamic_labels import *    

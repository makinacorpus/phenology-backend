#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
# Create your models here.


#########


#espece
class Species(models.Model):
    name = models.CharField(max_length=100, verbose_name="nom")
    description = models.CharField(max_length=500)
    pictures = models.CharField(max_length=300)

    class Meta:
        verbose_name = "espèce"
        verbose_name_plural = "espèces"

###########


#observateur
class Observer(models.Model):
    city = models.CharField(max_length=100, verbose_name="commune")
    fonction = models.CharField(max_length=70)
    adresse = models.CharField(max_length=80)
    codepostal = models.CharField(max_length=6, verbose_name="code postal")
    nationality = models.CharField(max_length=100, verbose_name="nationalité")
    phone = models.CharField(max_length=20)
    user = models.OneToOneField(User)
    is_crea = models.BooleanField(verbose_name="est un membre de crea")

    class Meta:
        verbose_name = "observateur"
        verbose_name_plural = "observateurs"


"""
#organisme
class Organization(models.Model):
    city = models.CharField(max_length=100, verbose_name="commune")
    activite = models.CharField(max_length=70)
    adresse = models.CharField(max_length=80)
    codepostal = models.CharField(max_length=6, verbose_name="code postal")
    nationality = models.CharField(max_length=100, verbose_name="nationalité")

    class Meta:
        verbose_name = "organisme"
        verbose_name_plural = "organismes"
"""


#zone:
class Area(models.Model):
    name = models.CharField(max_length=100, verbose_name="nom")
    codezone = models.CharField(max_length=20, verbose_name="code zone")
    polygone = models.CharField(max_length=500, verbose_name="polygone sig")
    lat = models.FloatField(verbose_name="lattitude")
    lon = models.FloatField(verbose_name="longitude")
    remark = models.CharField(max_length=100, verbose_name="remarque", blank=True)
    commune = models.CharField(max_length=100, verbose_name="commune")
    observers = models.ManyToManyField(Observer, verbose_name="Observateurs", blank=True)
    species = models.ManyToManyField(Species, blank=True)

    class Meta:
        verbose_name = "zone observation"
        verbose_name_plural = "zones observation"


##########

#individu
class Individual(models.Model):
    species = models.ForeignKey(Species, verbose_name="espece")
    area = models.ForeignKey(Area, verbose_name="zone")
    lat = models.FloatField(verbose_name="lattitude")
    lon = models.FloatField(verbose_name="longitude")
    remark = models.CharField(max_length=100, verbose_name="remarque")

    class Meta:
        verbose_name = "individu"
        verbose_name_plural = "individus"


#enneigement
class Snowing(models.Model):
    area = models.ForeignKey(Area, verbose_name="zone observation")
    observer = models.ForeignKey(Observer, verbose_name="observateur")
    date = models.DateTimeField(verbose_name="date saise")
    remark = models.CharField(max_length=100, verbose_name="remarque")
    height = models.FloatField(verbose_name="hauteur relevée")
    temperature = models.FloatField(verbose_name="température relevée")

    class Meta:
        verbose_name = "enneigement"
        verbose_name_plural = "enneigements"


#stades
class Stage(models.Model):
    name = models.CharField(max_length=100)
    species = models.ForeignKey(Species)
    month_beginning = models.IntegerField()
    order = models.IntegerField()
    pictures = models.CharField(max_length=300)


#observation
class Survey(models.Model):
    individual = models.ForeignKey(Individual, verbose_name="individu")
    observer = models.ForeignKey(Observer, verbose_name="observateur")
    stage = models.CharField(max_length=300, verbose_name="stade développement")
    date = models.DateTimeField(verbose_name="date saisie")
    remark = models.CharField(max_length=100, verbose_name="remarque")

    class Meta:
        verbose_name = "observation"
        verbose_name_plural = "observations"

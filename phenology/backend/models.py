#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from cStringIO import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile
import unicodedata
# Create your models here.


#########

def create_thumb(image, size):
    """Returns the image resized to fit inside a box of the given size"""
    image.thumbnail(size, Image.ANTIALIAS)
    temp = StringIO()
    image.save(temp, 'png')
    temp.seek(0)
    return SimpleUploadedFile('temp', temp.read())


def has_changed(instance, field, manager='objects'):
    """Returns true if a field has changed in a model

    May be used in a model.save() method.

    """
    if not instance.pk:
        return True
    manager = getattr(instance.__class__, manager)
    old = getattr(manager.get(pk=instance.pk), field)
    return not getattr(instance, field) == old


#espece
class Species(models.Model):
    name = models.CharField(max_length=100, verbose_name="nom")
    description = models.TextField(max_length=500)
    picture = models.ImageField(upload_to='picture/species',
                                default='no-img.jpg')

    def save(self, *args, **kwargs):
        # Save this photo instance
        if has_changed(self, 'picture') and self.picture:
            # on va convertir l'image en jpg
            #filename = os.path.splitext(os.path.split(self.picture.name)[-1])[0]
            filename = "%s.png" % unicodedata.normalize('NFD', self.name).lower()
            if(self.picture.file):
                image = Image.open(self.picture.file)
                """
                if image.mode not in ('L', 'RGB'):
                    image = image.convert('RGB')
                """
                # d'abord la photo elle-même
                self.picture.save(filename,
                                  create_thumb(image, (60, 80)),
                                  save=False)
        super(Species, self).save()


    class Meta:
        verbose_name = "espèce"
        verbose_name_plural = "espèces"

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
###########


#zone:
class Area(models.Model):
    name = models.CharField(max_length=100, verbose_name="nom")
    codezone = models.CharField(max_length=20, verbose_name="code zone")
    polygone = models.CharField(max_length=500, verbose_name="polygone sig")
    lat = models.FloatField(verbose_name="lattitude")
    lon = models.FloatField(verbose_name="longitude")
    altitude = models.FloatField(verbose_name="altitude", null=True, blank=True)
    remark = models.CharField(max_length=100, verbose_name="remarque", blank=True)
    commune = models.CharField(max_length=100, verbose_name="commune")
    species = models.ManyToManyField(Species, blank=True)

    class Meta:
        verbose_name = "zone observation"
        verbose_name_plural = "zones observation"

    def __str__(self):
        return "Area : %s [%s]" % (self.name, self.commune)


#observateur
class Observer(models.Model):
    user = models.OneToOneField(User)
    city = models.CharField(max_length=100, verbose_name="commune")
    fonction = models.CharField(max_length=70)
    adresse = models.CharField(max_length=80)
    codepostal = models.CharField(max_length=6, verbose_name="code postal")
    nationality = models.CharField(max_length=100, verbose_name="nationalité")
    phone = models.CharField(max_length=20)
    is_crea = models.BooleanField(verbose_name="est un membre de crea", default=False)
    is_active = models.BooleanField(verbose_name="est-il actif?", default=True)
    areas = models.ManyToManyField(Area, verbose_name="Zones", blank=True)
    date_inscription = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "observateur"
        verbose_name_plural = "observateurs"

    def __str__(self):
        return self.user.username

##########


#individu
class Individual(models.Model):
    name = models.CharField(max_length=100, verbose_name="nom")
    species = models.ForeignKey(Species, verbose_name="espece")
    area = models.ForeignKey(Area, verbose_name="zone")
    is_dead = models.BooleanField(verbose_name="est-il mort?", default=False)
#    observer = models.ForeignKey(Observer)
    lat = models.FloatField(verbose_name="latitude")
    lon = models.FloatField(verbose_name="longitude")
    altitude = models.FloatField(verbose_name="altitude", null=True, blank=True)
    circonference = models.FloatField(verbose_name="circonference", null=True, blank=True)

    remark = models.CharField(max_length=100, verbose_name="remarque")

    class Meta:
        verbose_name = "individu"
        verbose_name_plural = "individus"

    def __unicode__(self):
        return "%s %s" % (self.species.name, self.area.name)

    def __str__(self):
        return "%s %s" % (self.species.name, self.area.name)


#enneigement
class Snowing(models.Model):
    area = models.ForeignKey(Area, verbose_name="zone observation")
    observer = models.ForeignKey(Observer, verbose_name="observateur")
    date = models.DateTimeField(verbose_name="date saise")
    remark = models.CharField(max_length=100, verbose_name="remarque", default="", blank=True)
    height = models.FloatField(verbose_name="hauteur relevée")
    temperature = models.FloatField(verbose_name="température relevée", null=True, blank=True)

    class Meta:
        verbose_name = "enneigement"
        verbose_name_plural = "enneigements"


#stades
class Stage(models.Model):
    name = models.CharField(max_length=100)
    species = models.ForeignKey(Species)
    date_start = models.DateField(blank=True, null=True)
    month_start = models.IntegerField(blank=True, null=True)
    day_start = models.IntegerField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)
    month_end = models.IntegerField(blank=True, null=True,)
    day_end = models.IntegerField(blank=True, null=True)
    order = models.IntegerField()
    picture_before = models.ImageField(upload_to='picture/stages',
                                       default='no-img.jpg')
    picture_current = models.ImageField(upload_to='pictures/stages',
                                        default='no-img.jpg')
    picture_after = models.ImageField(upload_to='pictures/stages',
                                      default='no-img.jpg')

    def __str__(self):
        return "%s [%s] %s" % (self.name, self.species, self.order)


#observation
class Survey(models.Model):
    individual = models.ForeignKey(Individual, verbose_name="individu")
#    observer = models.ForeignKey(Observer, verbose_name="observateur")
    stage = models.ForeignKey(Stage, verbose_name="stade de développement")

    answer = models.CharField(max_length=300, verbose_name="reponse", blank=True)
    date = models.DateField(verbose_name="date saisie")
    remark = models.CharField(max_length=100, verbose_name="remarque", blank=True)

    class Meta:
        verbose_name = "observation"
        verbose_name_plural = "observations"


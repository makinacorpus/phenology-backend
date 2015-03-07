#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.utils import translation
from django.db import connection
import simplejson as json
from backend import logger
from backend import models

mapping = {'Meleze': 'Mélèze',
           'Epicea': 'Epicéa',
           'Bouleauv': 'Bouleau verruqueux',
           'Bouleaup': 'Bouleau pubescent',
           'Frene': 'Frêne',
           'Noisetier': 'Noisetier',
           'Tussilage': 'Tussilage',
           'Primevere': 'Primevère',
           'Sorbier': 'Sorbier',
           'Lilas': 'Lilas',
           'debourrement': 'Débourrement',
           'floraison': 'Floraison',
           'feuillaison': 'Feuillaison',
           'couleur_deb': 'Changement couleur début',
           'couleur_moit': 'Changement couleur moitié',
           'chute_fin': 'Chute des feuilles fin',
           'chute_moit': 'Chute des feuilles moitié'}


class Command(BaseCommand):
    help = "Dump data from real"

    def execute(self, *args, **options):
        """ Execute command """
        if("dump" in args):
            self.dump()
        else:
            self.load()
        logger.info('Done.')

    def dump(self):
        species = list(models.Species.objects.all().values("name", "picture", "description"))
        stages = list(models.Stage.objects.all().values("name", "picture_before", "picture_after", "picture_current", "species__name"))
        with open('backup_preprod.json', 'w') as fp:
            json.dump({
                "species": species,
                "stages": stages},
                fp)

    def load(self):
        """ integrate data in new db """
        with open('backup_preprod.json', 'r') as fp:
            data = json.load(fp)
            sp = models.Species.objects.filter(name="").first()

            for s in data["species"]:
                sp = models.Species.objects.filter(name=s["name"]).first()
                if sp:
                    sp.description = unicode(s["description"])
                    sp.picture = unicode(s["picture"])
                    print unicode(sp.name)
                    sp.save()
            for s in data["stages"]:
                sp = models.Stage.objects.filter(species__name=s["species__name"]).filter(name=s["name"]).first()
                if sp:
                    sp.picture_current = unicode(s["picture_current"])
                    sp.picture_before = unicode(s["picture_before"])
                    sp.picture_after = unicode(s["picture_after"])
                    sp.save()
                else:
                    print "stage not found"
        """
        cursor = connection.cursor()

        for key, value in mapping.items():
            cursor.execute("UPDATE backend_species SET name_fr='" + value +"' WHERE name='"+key +"'")
            cursor.execute("UPDATE backend_stage SET name_fr='" + value +"' WHERE name='"+key +"'")
        cursor.execute("UPDATE backend_stage SET is_active=0 WHERE name='chute_moit' OR name='chute_fin'")
        """
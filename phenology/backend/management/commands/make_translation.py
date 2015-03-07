#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.utils import translation
from django.db import connection

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

        self.integrate_translation()
        logger.info('Done.')

    def integrate_translation(self):
        """ integrate data in new db """
        cursor = connection.cursor()

        for key, value in mapping.items():
            cursor.execute("UPDATE backend_species SET name_fr='" + value +"' WHERE name='"+key +"'")
            cursor.execute("UPDATE backend_stage SET name_fr='" + value +"' WHERE name='"+key +"'")
        cursor.execute("UPDATE backend_stage SET is_active=0 WHERE name='chute_moit' OR name='chute_fin'")

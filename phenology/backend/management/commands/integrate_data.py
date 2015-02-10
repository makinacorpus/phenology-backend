#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from django.core.management.base import BaseCommand

from backend import logger
from backend import models


class Command(BaseCommand):
    help = "Dump data from real"

    def execute(self, *args, **options):
        """ Execute command """
        filename = "backup_db.json"
        self.integrate_dump_in_db(filename)
        logger.info('Done.')

    def integrate_dump_in_db(self, filename):
        """ integrate data in new db """
        outfile = open(filename)
        main_results = json.load(outfile)
        for species in main_results["species"]:
            species["name"] = species["name"].capitalize()
            if not models.Species.objects.filter(name=species["name"]):
                species_tmp = models.Species()
                species_tmp.name = species["name"]
                species_tmp.picture = species.get("picture")
                species_tmp.save()
                for i, stages in enumerate(species["stages"]):
                    stage_tmp = models.Stage()
                    stage_tmp.name = stages["stade"]
                    stage_tmp.order = i
                    stage_tmp.date_start = stages.get("date_start")
                    stage_tmp.month_start = stages.get("month_start")
                    stage_tmp.day_start = stages.get("day_start")
                    stage_tmp.date_end = stages.get("date_end")
                    stage_tmp.month_end = stages.get("month_end")
                    stage_tmp.day_end = stages.get("day_end")
                    stage_tmp.species = species_tmp
                    stage_tmp.save()
            else:
                species_tmp = models.Species.objects\
                    .filter(name=species["name"]).first()
            species_tmp.save()

        for code in sorted(main_results["codes"].keys()):
            """if code != "ronce":
                continue"""
            users = main_results["codes"][code]["users"]
            observers = []
            for user in users:
                general_user = user.get("username", user["nom_obs"])
                if not models.User.objects.filter(username=general_user):
                    user_tmp = models.User()
                    user_tmp.username = general_user
                    user_tmp.set_password(user["code"])
                    user_tmp.first_name = user["prenom_obs"]
                    user_tmp.last_name = user["nom_obs"]
                    user_tmp.email = user["email_obs"]
                    user_tmp.save()
                else:
                    user_tmp = models.User.objects.filter(username=general_user).first()

                if not models.Observer.objects.filter(user=user_tmp):
                    observer = models.Observer()
                    observer.user = user_tmp
                    observer.city = user["ville_obs"]
                    observer.codepostal = user["codepostal_obs"]
                    observer.nationality = user["nationalite_obs"]
                    observer.phone = user["tel_obs"]
                    observer.function = user["fonction_obs"]
                    observer.organism = user["organisme"]
                    observer.category = user["categorie"]
                    observer.adresse = user["adresse_obs"]
                    observer.is_active = user["is_active"]
                    observer.date_inscription = user["date_inscription"]
                    observer.is_crea = user.get("membre_crea", "non") == "oui"
                    observer.save()
                else:
                    observer = models.Observer.objects.filter(user=user_tmp).first()
                observers.append(observer)

            areas = main_results["codes"][code]["areas"]

            for area in areas:
                print area["name"]
                if not models.Area.objects.filter(name=area["name"]):
                    area_tmp = models.Area()
                    area_tmp.name = area["name"]
                    area_tmp.lat = str(area.get("lat")).replace(",",".")
                    area_tmp.lon = str(area.get("lon")).replace(",",".")
                    area_tmp.altitude = area.get("altitude")
                    area_tmp.commune = area.get("commune", "")
                    area_tmp.postalcode = area.get("code_postal", "")
                else:
                    area_tmp = models.Area.objects.filter(name=area["name"]).first()
                area_tmp.save()

                for observer in observers:
                    if(observer not in area_tmp.observer_set.all()):
                        area_tmp.observer_set.add(observer)

                area_tmp.save()

                for area_species in area["species"]:
                    species_m = [sp for sp in main_results["species"] if sp["name"] == area_species["name"].capitalize()]
                    species = models.Species.objects\
                        .filter(name=species_m[0]["name"]).first()
                    if(not species in area_tmp.species.all()):
                        area_tmp.species.add(species)
                    for ind in area_species["individuals"]:
                        if(not models.Individual.objects.filter(name=ind["name"]).filter(area_id=area_tmp.id).filter(species_id=species.id)):
                            ind_tmp = models.Individual()
                            ind_tmp.species = species
                            ind_tmp.area = area_tmp
                            ind_tmp.name = ind["name"]
                            ind_tmp.circonference = ind.get("circonference")
                            ind_tmp.altitude = ind.get("altitude")
                            ind_tmp.lat = ind.get("lat", "1")
                            ind_tmp.lon = ind.get("lon", "-1")
                            ind_tmp.save()
                        else:
                            ind_tmp = models.Individual.objects.filter(name=ind["name"]).filter(area_id=area_tmp.id).filter(species_id=species.id).first()

                        for survey in ind["surveys"]:
                            if(survey["stade"] == u"débourrement"):
                                survey["stade"] = "debourrement"
                            if(survey["stade"] == u"feuilaison"):
                                survey["stade"] = "feuillaison"
                            survey["stade"] = survey["stade"].strip()
                            survey_tmp = models.Survey()
                            survey_tmp.individual = ind_tmp
                            survey_tmp.firstname_obs = survey["prenom_obs"]
                            survey_tmp.name_obs = survey["nom_obs"]
                            survey_tmp.answer = "isObserved"
                            survey_tmp.date = survey["date"]
                            try:
                                survey_tmp.stage = models.Stage.objects.filter(name=survey["stade"]).filter(species_id=species.id).first()
                            except Exception as e:
                                print e
                            survey_tmp.save()
                area_tmp.save()

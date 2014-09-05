from backend import models
from datetime import datetime
import json


def create_sample_data():
    demo_data = {

            'species': [
                {
                    'name': "Noisetier",
                    'picture': "picture/species/noisetier.png",
                    'id': 'spec1',
                    'stages': [
                        {
                            'id': 'stageA1',
                            'name': "Flowering",
                            'date_start': '2014/01/15',
                            'date_end': '2014/03/31',
                            'month_start': '1',
                            'day_start': '15',
                            'month_end': '3',
                            'day_end': '31',
                            'order': "1",
                            'picture_before':
                                        "picture/stages/noisetier_s1_1.png",
                            'picture_current':
                                        "picture/stages/noisetier_s1_2.png",
                            'picture_after':
                                        "picture/stages/noisetier_s1_3.png"
                        },
                        {
                            'id': 'stageA2',
                            'name': "Blooming",
                            'date_start': '2014/02/15',
                            'date_end': '2014/04/30',
                            'month_start': '2',
                            'day_start': '15',
                            'month_end': '4',
                            'day_end': '30',
                            'order': "2",
                            'picture_before':
                                        "picture/stages/noisetier_s2_1.png",
                            'picture_current':
                                        "picture/stages/noisetier_s2_2.png",
                            'picture_after':
                                        "picture/stages/noisetier_s2_3.png"
                        },
                        {
                            'id': 'stageA3',
                            'name': "Leafing",
                            'date_start': '2014/03/15',
                            'date_end': '2014/05/31',
                            'month_start': '3',
                            'day_start': '15',
                            'month_end': '5',
                            'day_end': '31',
                            'order': '3',
                            'picture_before':
                                        "picture/stages/noisetier_s3_1.png",
                            'picture_current':
                                        "picture/stages/noisetier_s3_2.png",
                            'picture_after':
                                        "picture/stages/noisetier_s3_3.png"
                        }
                    ]
                },
                {
                    'name': "Meleze",
                    'id': 'spec2',
                    'picture': "picture/species/meleze.png",
                    'stages': [
                        {
                            'id': 'stageB1',
                            'name': "Blooming",
                            'order': '1'
                        },
                        {
                            'id': 'stageB2',
                            'name': "Fall",
                            'order': '2'
                        },
                        {
                            'id': 'stageB4',
                            'name': "End",
                            'order': '3'
                        }

                    ]
                },
                {
                    'name': "Tussilage",
                    'id': 'spec3',
                    'picture': "picture/species/tussilage.png",
                    'stages': [
                        {
                            'id': 'stageC1',
                            'name': 'Flowering Tussilage',
                            'date_start': '2014/02/10',
                            'date_end': '2014/05/31',
                            'month_start': '3',
                            'day_start': '15',
                            'month_end': '5',
                            'day_end': '31',
                            'order': '3',
                            'picture_before':
                                        "picture/stages/tussilage_s1_1.png",
                            'picture_current':
                                        "picture/stages/tussilage_s1_2.png",
                            'picture_after':
                                        "picture/stages/tussilage_s1_3.png"
                        }
                    ]
                }
            ],
            'areas': [
                {
                    'name': "Deep forest",
                    'id': 'area1',
                    'lat': 44.843792,
                    'lon': 6.255593,
                    'geojson': {
                          "type": "FeatureCollection",
                          "features": [
                            {
                              "type": "Feature",
                              "properties": {},
                              "geometry": {
                                "type": "Polygon",
                                "coordinates": [
                                  [
                                    [
                                      6.255115270614623,
                                      44.84452790096239
                                    ],
                                    [
                                      6.256048679351807,
                                      44.84442901000019
                                    ],
                                    [
                                      6.25645637512207,
                                      44.84393455264287
                                    ],
                                    [
                                      6.256166696548462,
                                      44.84334880535878
                                    ],
                                    [
                                      6.254600286483764,
                                      44.84342487677113
                                    ],
                                    [
                                      6.254514455795288,
                                      44.844193192405285
                                    ],
                                    [
                                      6.255115270614623,
                                      44.84452790096239
                                    ]
                                  ]
                                ]
                              }
                            }
                          ]
                        },
                    'species': [
                        {
                            'id': 'spec1',
                            'individuals': [
                                {
                                    'id': 'ind1',
                                    'name': "Noisetier A 1",
                                    'lat': 44.843788,
                                    'lon': 6.256015,
                                },
                                {
                                    'id': 'ind2',
                                    'name': "Noisetier A 2",
                                    'lat': 44.843818,
                                    'lon': 6.254878,
                                },
                                {
                                    'id': 'ind3',
                                    'name': "Noisetier A 3",
                                    'lat': 44.843506,
                                    'lon': 6.254819,
                                },
                            ]
                        },
                        {
                            'id': 'spec2',
                            'individuals': [
                                {
                                    'id': 'ind1',
                                    'name': "Meleze B 1"
                                },
                                {
                                    'id': 'ind2',
                                    'name': "Meleze B 2"
                                },

                                {
                                    'id': 'ind3',
                                    'name': "Meleze B 3"
                                },
                            ]
                        },
                        {
                            'id': 'spec3',
                            'individuals': [
                                {
                                    'id': 'ind1',
                                    'name': "Tussilage C 1"
                                },
                                {
                                    'id': 'ind2',
                                    'name': "Tussilage C 2"
                                },

                                {
                                    'id': 'ind3',
                                    'name': "Tussilage C 3"
                                },
                            ]
                        }
                    ]
                },
                {
                    'name': "Area 2",
                    'id': 'area2',
                    'lat': 44.92528028397075,
                    'lon': 6.639003753662109,
                    'geojson': {
                      "type": "FeatureCollection",
                      "features": [
                        {
                          "type": "Feature",
                          "properties": {},
                          "geometry": {
                            "type": "Polygon",
                            "coordinates": [
                              [
                                [
                                  6.63325309753418,
                                  44.925614521068866
                                ],
                                [
                                  6.635527610778809,
                                  44.92117812483123
                                ],
                                [
                                  6.644110679626465,
                                  44.92199858009217
                                ],
                                [
                                  6.645998954772949,
                                  44.925827216391475
                                ],
                                [
                                  6.64170742034912,
                                  44.92889601838952
                                ],
                                [
                                  6.634325981140137,
                                  44.92886563501494
                                ],
                                [
                                  6.63325309753418,
                                  44.925614521068866
                                ]
                              ]
                            ]
                          }
                        },
                      ]
                    },
                    'species': [
                        {
                            'id': 'spec1',
                            'individuals': [
                                {
                                    'id': 'ind1',
                                    'name': "Tree A 1",
                                    'lat': 44.9264349129738,
                                    'lon': 6.637372970581054,
                                },
                                {
                                    'id': 'ind2',
                                    'name': "Tree A 2",
                                    'lat': 44.92479411744738,
                                    'lon': 6.638617515563965,
                                },
                                {
                                    'id': 'ind4',
                                    'name': "Tree A 3",
                                    'lat': 44.92303172930961,
                                    'lon': 6.637394428253174,
                                }
                            ]
                        },
                        {
                            'id': 'spec2',
                            'individuals': [
                                {
                                    'id': 'ind1',
                                    'name': "Tree B 1",
                                    'lat': 44.92743759827963,
                                    'lon': 6.639432907104492,
                                },
                                {
                                    'id': 'ind2',
                                    'name': "Tree B 2",
                                    'lat': 44.92622221990126,
                                    'lon': 6.639432907104492,
                                },
                                {
                                    'id': 'ind3',
                                    'name': "Tree B 3",
                                    'lat': 44.92673875885417,
                                    'lon': 6.638617515563965,
                                }
                            ]
                        }
                    ]
                }
            ]
    }
    user = models.User.objects.filter(username="admin").first()
    if not models.Observer.objects.filter(user=user):
        observer = models.Observer()
        observer.user = user
        observer.is_crea = True
        observer.save()
    else:
        observer = models.Observer.objects.filter(user=user).first()

    for species in demo_data["species"]:
        if not models.Species.objects.filter(name=species["name"]):
            species_tmp = models.Species()
            species_tmp.name = species["name"]
            species_tmp.picture = species.get("picture")
            species_tmp.save()
        else:
            species_tmp = models.Species.objects\
                .filter(name=species["name"]).first()
        for stage in species["stages"]:
            if not models.Stage.objects.filter(name=stage["name"]):
                stage_tmp = models.Stage()
                stage_tmp.name = stage["name"]
                stage_tmp.species = species_tmp
                if stage.get("date_start"):
                    stage_tmp.date_start = datetime.strptime(
                        stage.get("date_start"), "%Y/%m/%d")
                stage_tmp.month_start = stage.get("month_start")
                stage_tmp.day_start = stage.get("day_start")
                stage_tmp.month_end = stage.get("month_end")
                stage_tmp.day_end = stage.get("month_end")
                if stage.get("picture_before"):
                    stage_tmp.picture_before = stage.get("picture_before")
                if stage.get("picture_current"):
                    stage_tmp.picture_current = stage.get("picture_current")
                if stage.get("picture_after"):
                    stage_tmp.picture_after = stage.get("picture_after")
                if stage.get("date_end"):
                    stage_tmp.date_end = datetime.strptime(
                        stage.get("date_end"), "%Y/%m/%d")
                stage_tmp.order = stage["order"]
                stage_tmp.save()
    species_tmp.save()
    for area in demo_data["areas"]:
        if not models.Area.objects.filter(name=area["name"]):
            area_tmp = models.Area()
            area_tmp.name = area["name"]
            area_tmp.lat = area.get("lat", "-1")
            area_tmp.lon = area.get("lon", "1")
            polygon = json.dumps(area.get("geojson", {}))
            area_tmp.polygone = polygon
        else:
            area_tmp = models.Area.objects.filter(name=area["name"]).first()
        area_tmp.save()

        if(not observer in area_tmp.observer_set.all()):
            area_tmp.observer_set.add(observer)

        area_tmp.save()
        for area_species in area["species"]:
            species_m = [sp for sp in demo_data["species"] if sp["id"] == area_species["id"]]
            species = models.Species.objects\
                .filter(name=species_m[0]["name"]).first()
            if(not species in area_tmp.species.all()):
                area_tmp.species.add(species)
            for ind in area_species["individuals"]:
                if(not models.Individual.objects.filter(name=ind["name"])):
                    ind_tmp = models.Individual()
                    ind_tmp.species = species
                    ind_tmp.area = area_tmp
                    ind_tmp.name = ind["name"]
                    ind_tmp.lat = ind.get("lat", "1")
                    ind_tmp.lon = ind.get("lon", "-1")
                    ind_tmp.observer = observer
                    ind_tmp.save()
        area_tmp.save()

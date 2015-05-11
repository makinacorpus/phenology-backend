#!/usr/bin/env python
# -*- coding: utf-8 -*-

from import_export import resources
from backend import models
from django.utils.translation import ugettext


class AreaResource(resources.ModelResource):

    class Meta:
        model = models.Area
        exclude = ('species', 'codezone', )


class SpeciesResource(resources.ModelResource):

    class Meta:
        model = models.Species


class SnowingResource(resources.ModelResource):

    class Meta:
        model = models.Snowing


class SurveyResource(resources.ModelResource):

    class Meta:
        model = models.Survey
        fields = (
            "id",
            "date",
            "individual__name",
            "individual__species__name",
            "stage__name",
            "individual__area__name",
            "individual__area__commune",
            "answer",
            "remark",
        )
        export_order = fields

    def dehydrate_answer(self, survey):
        # translate survey answer
        return ugettext(survey.answer)

    def export(self, queryset=None):
        # optimize queryset
        queryset = queryset.select_related("stage", "individual",
                                           "individual__species",
                                           "individual__area")
        return super(SurveyResource, self).export(queryset)


class ObserverResource(resources.ModelResource):

    class Meta:
        model = models.Observer
        fields = (
            "id",
            "user",
            "user__username",
            'user__first_name',
            'user__last_name',
            'user__email',
            "city",
            "fonction",
            "adresse",
            "codepostal",
            "nationality",
            "organism",
            "category",
            "phone",
            "mobile",
            "is_crea",
            "is_active",
            "areas",
            "date_inscription",
        )
        export_order = fields

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from backend import models
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from import_export.admin import ImportExportModelAdmin
from backend import ressources
from backoffice import forms
from django.db.models import Count


class TabAdmin(TranslationAdmin):
    class Media:
        js = (
            '/static/modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('/static/modeltranslation/css/tabbed_translation_fields.css',),
        }


class StageAdmin(TabAdmin, ImportExportModelAdmin):
    list_display = ('name', 'species', 'order', 'is_active', )
    search_fields = ['name', 'species__name']
    ordering = ('species', 'order', 'name')


class SurveyAdmin(ImportExportModelAdmin):
    list_display = ('date', 'ind_name', 'species_name',
                    'stage_name', '_answer', 'remark', 'area_name')
    search_fields = ['date', 'individual__name', 'individual__species__name',
                     'stage__name', 'answer', 'remark', 'individual__area__name']

    def _answer(self, obj):
        return ugettext(obj.answer)
    _answer.short_description = _('Answer')
    _answer.admin_order_field = 'answer'

    def ind_name(self, obj):
        return ("%s" % (obj.individual.name))
    ind_name.short_description = _('Individual')
    ind_name.admin_order_field = 'individual__name'

    def species_name(self, obj):
        return ("%s" % (obj.individual.species.name))
    species_name.short_description = _('Species')
    species_name.admin_order_field = 'individual__species__name'

    def area_name(self, obj):
        return ("%s" % (obj.individual.area.name))
    area_name.short_description = _('Area')
    area_name.admin_order_field = 'individual__area__name'

    def stage_name(self, obj):
        return ("%s" % (obj.stage.name))
    stage_name.short_description = _('Stage')
    stage_name.admin_order_field = 'stage__name'

admin.site.register(models.Survey, SurveyAdmin)


class IndividualAdmin(ImportExportModelAdmin):
    list_display = ('name', 'species', 'area', 'area_city')
    search_fields = ['name', 'species__name', 'area__name', 'area__commune']
    ordering = ('area', 'species', 'name',)

    def area_city(self, obj):
        return ("%s" % (obj.area.commune))
    area_city.short_description = _('Commune')
    area_city.admin_order_field = 'area__commune'

admin.site.register(models.Individual, IndividualAdmin)


class AreaAdmin(ImportExportModelAdmin):
    resource_class = ressources.AreaResource
    list_display = ('name', 'commune', 'altitude', 'species', 'observers',)
    search_fields = ['name', 'observer__user__username', 'altitude',
                     'individual__species__name', 'commune']
    ordering = ('name', 'commune', 'altitude', )
    form = forms.AreaAdminForm

    def observers(self, obj):
        return ",".join([str(o.user.username).strip()
                         for o in
                         obj.observer_set.all().select_related('user')])
    observers.short_description = _('Observers')

    def species(self, obj):
        return ",".join(set([unicode(o.species.name).strip()
                             for o in
                             obj.individual_set.all().
                             select_related('species')]))
    species.short_description = _('species')

admin.site.register(models.Area, AreaAdmin)


class SnowingAdmin(ImportExportModelAdmin):
    resource_class = ressources.SnowingResource
    list_display = ('date', 'area_city', 'height', 'remark')
    list_select_related = ('area', )

    def area_city(self, obj):
        return ("%s" % (obj.area.commune))
    area_city.short_description = _('Commune')

admin.site.register(models.Snowing, SnowingAdmin)


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UserInline(admin.StackedInline):
    model = models.User
    can_delete = False


# Define a new User admin
class ObserverAdmin(ImportExportModelAdmin):
    resource_class = ressources.ObserverResource
    list_display = ('username', 'last_name', 'first_name', 'city', 'organism',
                    'category', 'codepostal', 'nb_inds', 'nb_areas',
                    'nb_surveys')
    search_fields = ['city', 'user__first_name', 'user__last_name',
                     'codepostal']
    list_select_related = ('user', )

    def queryset(self, request):
        qs = super(ObserverAdmin, self).queryset(request)
        qs = qs.annotate(Count('areas__individual__survey'))
        qs = qs.annotate(Count('areas__individual'))
        qs = qs.annotate(Count('areas'))
        return qs

    def first_name(self, obj):
        return (obj.user.first_name)
    first_name.admin_order_field = 'user__first_name'
    first_name.short_description = _('first name')

    def last_name(self, obj):
        return (obj.user.last_name)
    last_name.admin_order_field = 'user__last_name'
    last_name.short_description = ugettext('last name')

    def username(self, obj):
        if(obj.user):
            return obj.user.last_name
    username.admin_order_field = 'user__username'
    username.short_description = ugettext('username')

    def nb_inds(self, obj):
        return models.Individual.objects.filter(area__observer=obj).count()
    nb_inds.admin_order_field = 'areas__individual__count'

    def nb_areas(self, obj):
        return models.Area.objects.filter(observer=obj).count()
    nb_areas.admin_order_field = 'areas__count'

    def nb_surveys(self, obj):
        return models.Survey.objects.filter(individual__area__observer=obj).count()
    nb_surveys.admin_order_field = 'areas__individual__survey__count'

admin.site.register(models.Observer, ObserverAdmin)


class StageInline(TranslationTabularInline):
    model = models.Stage
    extra = 0


class StageInline2(StageInline):
    ordering = ("order",)


class SpeciesAdmin(TabAdmin, ImportExportModelAdmin):
    list_display = ('name', 'nb_stages', 'nb_surveys', 'nb_observers')
    inlines = (StageInline2, )

    def nb_stages(self, obj):
        return models.Stage.objects.filter(species=obj).count()
    nb_stages.short_description = "nb " + ugettext('Stages')

    def nb_surveys(self, obj):
        return models.Survey.objects.filter(individual__species=obj).count()
    nb_surveys.short_description = "nb " + ugettext('Surveys')

    def nb_observers(self, obj):
        return models.Observer.objects.filter(areas__individual__species=obj).count()
    nb_observers.short_description = "nb " + ugettext('Observers')

# Re-register UserAdmin
# admin.site.unregister(models.User)
# admin.site.register(models.User, UserAdmin)

admin.site.register(models.Stage, StageAdmin)
admin.site.register(models.Species, SpeciesAdmin)
# admin.site.register(models.Temperature)

from django.contrib import admin
from backend import models
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from import_export.admin import ImportExportModelAdmin
from backend import ressources

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
    list_display = ('date', 'individual', 'species_name', 'stage', 'answer', 'remark', 'area_name')

    def species_name(self, obj):
        return ("%s" % (obj.individual.species.name))
    species_name.short_description = _('Species')

    def area_name(self, obj):
        return ("%s" % (obj.individual.area.name))

    def stage_name(self, obj):
        return ("%s" % (obj.observer))
admin.site.register(models.Survey, SurveyAdmin)


class IndividualAdmin(ImportExportModelAdmin):
    list_display = ('name', 'species', 'area', 'area_city')
    search_fields = ['name', 'species__name', 'area__name', 'area__codezone']
    ordering = ('area', 'species', 'name',)

    def area_city(self, obj):
        return ("%s" % (obj.area.commune))

admin.site.register(models.Individual, IndividualAdmin)


class AreaAdmin(ImportExportModelAdmin):
    resource_class = ressources.AreaResource
    list_display = ('name', 'observers', 'commune')
    search_fields = ['name', 'observer__user__username', 'species__name']

    def observers(self, obj):
        return ",".join([str(o.user.username).strip() for o in obj.observer_set.all().select_related('user')])

admin.site.register(models.Area, AreaAdmin)


class SnowingAdmin(ImportExportModelAdmin):
    resource_class = ressources.SnowingResource
    list_display = ('date', 'area_city', 'height', 'remark')
    list_select_related = ('area', )

    def area_city(self, obj):
        return ("%s" % (obj.area.commune))

admin.site.register(models.Snowing, SnowingAdmin)


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UserInline(admin.StackedInline):
    model = models.User
    can_delete = False


# Define a new User admin
class ObserverAdmin(ImportExportModelAdmin):
    inlines = (UserInline, )
    resource_class = ressources.ObserverResource
    list_display = ('last_name', 'first_name', 'city', )
    search_fields = ['city', 'user__first_name', 'user__last_name']
    #list_select_related = ('user', )
    #search_fields = ('user',)

    def first_name(self, obj):
        return (obj.user.first_name)

    def last_name(self, obj):
        return (obj.user.last_name)


admin.site.register(models.Observer, ObserverAdmin)


class StageInline(TranslationTabularInline):
    model = models.Stage
    extra = 0


class SpeciesAdmin(TabAdmin, ImportExportModelAdmin):
    inlines = (StageInline, )


# Re-register UserAdmin
# admin.site.unregister(models.User)
# admin.site.register(models.User, UserAdmin)

admin.site.register(models.Stage, StageAdmin)
admin.site.register(models.Species, SpeciesAdmin)
# admin.site.register(models.Temperature)

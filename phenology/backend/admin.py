from django.contrib import admin
from backend import models
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline


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


class StageAdmin(TabAdmin):
    list_display = ('name', 'species', 'order', 'is_active', )
    search_fields = ['name', 'species__name']
    ordering = ('species', 'order', 'name')


class SurveyAdmin(admin.ModelAdmin):
    list_display = ('date', 'individual', 'species_name', 'stage', 'answer', 'remark', 'area_name')

    def species_name(self, obj):
        return ("%s" % (obj.individual.species.name))
    species_name.short_description = _('Species')

    def area_name(self, obj):
        return ("%s" % (obj.individual.area.name))

    def stage_name(self, obj):
        return ("%s" % (obj.observer))
admin.site.register(models.Survey, SurveyAdmin)


class IndividualAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'area',)
    search_fields = ['name', 'species__name', 'area__name', 'area__codezone']
    ordering = ('area', 'species', 'name',)

admin.site.register(models.Individual, IndividualAdmin)


class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'observers',)
    search_fields = ['name', 'observer__user__username']

    def observers(self, obj):
        return [str(o.user.username) for o in obj.observer_set.all().select_related('user')]

admin.site.register(models.Area, AreaAdmin)


class SnowingAdmin(admin.ModelAdmin):
    list_display = ('date', 'area_city', 'height', 'remark')
    list_select_related = ('area', )

    def area_city(self, obj):
        return ("%s" % (obj.area.commune))

admin.site.register(models.Snowing, SnowingAdmin)


class ObserverAdmin(admin.ModelAdmin):
    list_display = ('user', )
    list_select_related = ('user', )

    def area_city(self, obj):
        return ("%s" % (obj.area.commune))

admin.site.register(models.Observer, ObserverAdmin)


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class EmployeeInline(admin.StackedInline):
    model = models.Observer
    can_delete = False
    verbose_name_plural = 'observer'


class StageInline(TranslationTabularInline):
    model = models.Stage
    extra = 0


# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (EmployeeInline, )


class SpeciesAdmin(TabAdmin):
    inlines = (StageInline, )


# Re-register UserAdmin
admin.site.unregister(models.User)
admin.site.register(models.User, UserAdmin)

admin.site.register(models.Stage, StageAdmin)
admin.site.register(models.Species, SpeciesAdmin)

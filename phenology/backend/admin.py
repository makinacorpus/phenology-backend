from django.contrib import admin
from backend import models
from django.contrib.auth.admin import UserAdmin
from modeltranslation.admin import TranslationAdmin

admin.site.register(models.Area)
admin.site.register(models.Species, TranslationAdmin)
admin.site.register(models.Individual)
admin.site.register(models.Observer)
admin.site.register(models.Survey)
admin.site.register(models.Snowing)


class StageAdmin(TranslationAdmin):
    list_display = ('name', 'species', 'order', 'is_active', )
    ordering = ('species', 'order', 'name')

admin.site.register(models.Stage, StageAdmin)


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class EmployeeInline(admin.StackedInline):
    model = models.Observer
    can_delete = False
    verbose_name_plural = 'observer'


# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (EmployeeInline, )

# Re-register UserAdmin
admin.site.unregister(models.User)
admin.site.register(models.User, UserAdmin)

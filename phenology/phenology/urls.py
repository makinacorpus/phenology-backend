from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework import routers
from backend import views

admin.autodiscover()

router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
#router.register(r'groups', views.GroupViewSet)
router.register(r'areas', views.AreaViewSet)
router.register(r'species', views.SpeciesViewSet)
router.register(r'observers', views.ObserverViewSet)
router.register(r'individuals', views.IndividualViewSet)
#router.register(r'user_setting', views.UserSettingsViewSet)

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'.*', include('backend.urls'))
)

from django.conf.urls import patterns, include, url, static
from django.contrib import admin

from rest_framework import routers
from backend import views
from phenology import settings

admin.autodiscover()

router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
#router.register(r'groups', views.GroupViewSet)
router.register(r'areas', views.AreaViewSet)
router.register(r'species', views.SpeciesViewSet)
router.register(r'observers', views.ObserverViewSet)
router.register(r'individuals', views.IndividualViewSet)
router.register(r'surveys', views.SurveyViewSet)

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^user_settings', views.user_settings, name='user_settings'),
    url(r'^user_surveys', views.user_surveys, name='user_surveys'),
    url(r'.*', include('backend.urls'))

) + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

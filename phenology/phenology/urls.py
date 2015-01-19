from django.conf.urls import patterns, include, url, static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from rest_framework import routers
from backend import views
from phenology import settings
from backoffice.urls import urls as backoffice_urls

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
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
        namespace='rest_framework')),
    url(r'^user_settings', views.user_settings, name='user_settings'),
    url(r'^user_surveys/(?P<pk>\d+)', views.SurveyDetail.as_view(),
        name='survey-detail'),
    url(r'^user_surveys', views.UserSurveyList.as_view(), name='user_surveys'),
    url(r'^user_snowcover/(?P<pk>\d+)', views.SnowCoverDetail.as_view(),
        name='snowcover-detail'),
    url(r'^user_snowcover', views.UserSnowCoverList.as_view(),
        name='user_snowcover'),
    url(r'^portail/', include(backoffice_urls)),
    url(r'^select2/', include('select2.urls')),
)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static.static(settings.MEDIA_URL,
                             document_root=settings.MEDIA_ROOT)

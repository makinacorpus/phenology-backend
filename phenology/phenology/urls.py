from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework import routers
from backend import views
from backend.models import Individual, Area, Observer, Organization, Survey, Snowing, Species

admin.autodiscover()
admin.site.register(Area)
admin.site.register(Species)
admin.site.register(Individual)
admin.site.register(Observer)
admin.site.register(Organization)
admin.site.register(Survey)
admin.site.register(Snowing)


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'backend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'.*', include('backend.urls'))
)

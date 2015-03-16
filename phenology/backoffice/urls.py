#!/usr/bin/env python
# -*- coding: utf-8 -*-
__docformat__ = 'restructuredtext en'

from django.conf.urls import patterns, url
from backoffice import views
from django.core.urlresolvers import reverse_lazy

import os
base_path = os.path.join(os.path.dirname(__file__))

print base_path

urls = patterns(
    '',
    # home
    url(r'^$', views.index, name='home'),

    # profile
    url(r'^profile', views.user_detail, name='profile'),
    url(r'^register', views.register_user, name='register'),

    # change password
    url(r'^password_change',
        'django.contrib.auth.views.password_change',
        {'template_name': base_path + '/templates/generic_form.html'}),
    url(r'^password_change/done',
        'django.contrib.auth.views.password_change_done',
        name='password_change_done'),

    # change password
    url(r'^password_reset', views.password_reset, name="password_reset"),
    # authentification
    url(r'^login',
        'django.contrib.auth.views.login',
        {'template_name': base_path + '/templates/login_form.html'},
        name='login'),
    url(r'^logout',
        'django.contrib.auth.views.logout',
        {"next_page": reverse_lazy('home')},
        name='logout'),

    # snowing
    url(r'^area/(?P<area_id>\d+)/snowing/create$', views.snowing_detail,
        name='snowing-detail'),
    url(r'^area/(?P<area_id>\d+)/snowing/(?P<snowing_id>\d+)',
        views.snowing_detail,
        name='snowing-detail'),

    # area
    url(r'^area/create$', views.area_detail, name='area-detail'),
    url(r'^area/(?P<area_id>\d+)', views.area_detail, name='area-detail'),

    # individual
    url(r'^individual/create$', views.individual_detail,
        name='individual-detail'),
    url(r'^individual/(?P<ind_id>\d+)', views.individual_detail,
        name='individual-detail'),

    # survey
    url(r'^survey/create$', views.survey_detail, name='survey-detail'),
    url(r'^survey/(?P<survey_id>\d+)', views.survey_detail,
        name='survey-detail'),

    # mysurveys
    url(r'^mysurveys$', views.dashboard, name='my-surveys'),
    url(r'^get_species_list$', views.get_species_list, name='species-list'),

    # datatable
    url(r'^allsurveys$', views.all_surveys, name='all-surveys'),
    url(r'^getsurveys$', views.get_surveys, name='get-surveys'),

    # map
    url(r'^map_all_surveys$', views.map_all_surveys, name='map-surveys'),
    url(r'^search_surveys', views.search_surveys, name="search-surveys"),

    # viz
    url(r'^viz_all_surveys$', views.viz_all_surveys, name='viz-surveys'),
    url(r'^get_data_for_viz$', views.get_data_for_viz, name='viz-data'),
    url(r'^viz_area_surveys$', views.viz_area_surveys,
        name='viz-area-surveys'),
    url(r'^get_area_data$', views.get_area_data, name='area-data'),


    # export
    url(r'^export_surveys', views.export_surveys, name="export-survey"),

    # map
    url(r'^map_all_snowings$', views.map_all_snowings, name='map-snowings'),
    url(r'^search_snowings', views.search_snowings, name="search-snowings"),
    url(r'^viz_snowings$', views.viz_snowings, name='viz-snowings'),
    url(r'^get_area_snowings$', views.get_area_snowings,
        name='viz-area-snowings'),
    url(r'^map_viz$', views.map_viz, name='viz-map'),
)
# vim:set et sts=4 ts=4 tw=80:

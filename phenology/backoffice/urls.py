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
    url(r'^$', views.index, name='home'),

    url(r'^profile', views.user_detail, name='profile'),
    url(r'^register', views.register_user, name='register'),

    url(r'^password_change',
        'django.contrib.auth.views.password_change',
        {'template_name': base_path + '/templates/generic_form.html'}),
    url(r'^password_change/done',
        'django.contrib.auth.views.password_change_done',
        name='password_change_done'),

    url(r'^login',
        'django.contrib.auth.views.login',
        {'template_name': base_path + '/templates/login_form.html'},
        name='login'),
    url(r'^logout',
        'django.contrib.auth.views.logout',
        {"next_page": reverse_lazy('home')},
        name='logout'),
    url(r'^export_surveys', views.export_surveys, name="export-survey"),
    url(r'^area/create$', views.area_detail, name='area-detail'),
    url(r'^area/(?P<area_id>\d+)', views.area_detail, name='area-detail'),

    url(r'^individual/create$', views.individual_detail,
        name='individual-detail'),
    url(r'^individual/(?P<ind_id>\d+)', views.individual_detail,
        name='individual-detail'),

    url(r'^survey/create$', views.survey_detail, name='survey-detail'),
    url(r'^survey/(?P<survey_id>\d+)', views.survey_detail,
        name='survey-detail'),

    url(r'^mysurveys$', views.dashboard, name='my-surveys'),
    url(r'^allsurveys$', views.all_surveys, name='all-surveys'),
    url(r'^getsurveys$', views.get_surveys, name='get-surveys'),
    # map
    url(r'^map_all_surveys$', views.map_all_surveys, name='map-surveys'),
    url(r'^search_surveys', views.search_surveys, name="search-surveys"),
)
# vim:set et sts=4 ts=4 tw=80:

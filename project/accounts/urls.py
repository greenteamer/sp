# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.conf.urls import patterns, include, url


urlpatterns = patterns('project.accounts.views',

    # Главная страница
    url(r'^$', 'profileView',
		{'template_name':'accounts/profile.html'},
		name='profileView'),
    url(r'^registration/$', 'registrationView',
		{'template_name':'accounts/registration.html'},
		name='registrationView'),


    url(r'^organizer/', include('project.accounts.urls_organizer')),

    # Страницы сайта
    # url(r'^(?P<slug>[-\w]+)/$', 'page_view',
    #     {'template_name':'main/page.html'},
    #     name='page_view'),
)

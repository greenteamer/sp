# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.conf.urls import patterns, url

urlpatterns = patterns('project.pristroy.views',

    # Главная страница раздела Пристрой
    url(r'^/$', 'Index',
		{'template_name': 'pristroy/index.html'},
		name='pristroy_catalog_home'),
    # категория
    url(r'^/(?P<category_slug>[-\w]+)/$', 'Index',
		{'template_name': 'pristroy/index.html'},
		name='pristroy_category'),

)

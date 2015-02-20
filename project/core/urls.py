# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.conf.urls import patterns, url

urlpatterns = patterns('project.core.views',
    # Главная страница
    url(r'^$', 'index_view',
		{'template_name':'core/index.html'},
		name='catalog_home'),
    # Страницы сайта
    # url(r'^(?P<slug>[-\w]+)/$', 'page_view',
    #     {'template_name':'main/page.html'},
    #     name='page_view'),
)

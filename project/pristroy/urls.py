# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.conf.urls import patterns, url

urlpatterns = patterns('project.pristroy.views',

    # категория
    # url(r'^category-(?P<category_slug>[-\w]+)/$', 'Category',
		# {'template_name': 'pristroy/category.html'},
		# name='category'),

    # Главная страница раздела Пристрой
    url(r'^$', 'Index',
		{'template_name': 'pristroy/index.html'},
		name='catalog_home'),

)

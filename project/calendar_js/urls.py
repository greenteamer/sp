# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.conf.urls import patterns, include, url

urlpatterns = patterns('project.calendar_js.views',

    # страница категорий
    url(r'^calendar/$', 'calendarView',
        {'template_name': 'calendar/calendar.html'},
        name='calendarView'),

    # страница одной категории
    # url(r'^category-(?P<category_slug>[-\w]+)/$', 'coreCategory',
    #     {'template_name': 'core/core_category.html'},
    #     name='category'),

    # # страница для обработки ajax запросов
    # url(r'^ajaxquery/$', 'ajaxquery', name='ajaxquery'),
    #
)
# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.conf.urls import patterns, include, url
from project import settings


urlpatterns = patterns('project.notifications.views',
    #
    # url(r'^all/$', 'noticeAllView',
    #    {'template_name': 'accounts/profile.html'},
    #    name='noticeAllView'),
    # url(r'^new/$', 'noticeFormView',
    #    {'template_name': 'accounts/registration.html'},
    #     name='noticeFormView'),
)
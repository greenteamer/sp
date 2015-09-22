# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.conf.urls import patterns, include, url

urlpatterns = patterns('project.client.views',

    url(r'^cart-items/$', 'getCartItems', name='client_home'),
    url(r'^push-question/$', 'pushQuestion', name='push_question'),
    url(r'^organizers/$', 'getOrganizers', name='custom_get_organizers'),
    url(r'^post-answer/$', 'postAnswer', name='post_answer')
)

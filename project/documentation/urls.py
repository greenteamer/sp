# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'project.documentation.views',
    url(r'^documentation/$', 'docView',
        {'template_name': 'decumentation/doc.html'},
        name='docView'),
)

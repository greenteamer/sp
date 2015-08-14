# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.conf.urls import patterns, include, url

urlpatterns = patterns('project.client.views',

    # Главная страница
    url(r'^$', 'indexView',
        {'template_name': 'client/pages/index.html'},
        name='client_home'),

    url(r'^catalog/$', 'catalogView',
        {'template_name': 'client/pages/catalog.html'},
        name='client_home'),

    url(r'^add-to-cart/$', 'clientAddToCartView',
        name='client_add_to_cart'),

    # api
    url(r'^v1/all-purchases/$', 'getAllPurchases', name='get-all-purchases'),
)

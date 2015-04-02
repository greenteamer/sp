# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.conf.urls import patterns, url

urlpatterns = patterns('project.cart.views',

    url(r'^cart/$', 'cartView',
		{'template_name': 'cart/core_cart.html'},
		name='cartView'),
    url(r'^purchases-cart/$', 'purchasesCartView',
		{'template_name': 'cart/core_purchases_cart.html'},
		name='purchasesCartView'),
)



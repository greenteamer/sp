# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.conf.urls import patterns, url


urlpatterns = patterns('project.accounts.views',

    url(r'^purchases/$', 'purchases',
		{'template_name': 'accounts/purchases.html'},
		name='purchases'),

    url(r'^purchase-add/$', 'purchaseAdd',
		{'template_name': 'accounts/purchase_add.html'},
		name='purchaseAdd'),

    url(r'^purchase-(\d+)/$', 'purchase',
		{'template_name': 'accounts/purchase.html'},
		name='purchase'),

    url(r'^purchase-(\d+)-edit$', 'purchase',
		{'template_name': 'accounts/purchase_edit.html',
         'edit': True},
		name='purchaseEdit'),


    url(r'^purchase-(?P<purchase_id>\d+)/catalogs$', 'catalogs',
		{'template_name': 'accounts/catalogs.html'},
		name='catalogs'),

    url(r'^purchase-(?P<purchase_id>\d+)/catalog-add/$', 'catalogAdd',
		{'template_name': 'accounts/catalog_add.html'},
		name='catalogAdd'),

    url(r'^purchase-(?P<purchase_id>\d+)/catalog-(?P<catalog_id>\d+)/$', 'catalog',
		{'template_name': 'accounts/catalog.html'},
		name='catalog'),


    url(r'^purchase-(?P<purchase_id>\d+)/catalog-(?P<catalog_id>\d+)/products$', 'products',
		{'template_name': 'accounts/products.html'},
		name='products'),

    url(r'^purchase-(\d+)/catalog-(?P<catalog_id>\d+)/product-add$', 'productAdd',
		{'template_name': 'accounts/product_add.html'},
		name='productAdd'),

    url(r'^purchase-(?P<purchase_id>\d+)/catalog-(?P<catalog_id>\d+)/product-(?P<product_id>\d+)$', 'product',
		{'template_name': 'accounts/product.html'},
		name='product'),

    url(r'^purchase-(?P<purchase_id>\d+)/catalog-(?P<catalog_id>\d+)/product-(?P<product_id>\d+)-edit$', 'product',
		{'template_name': 'accounts/product_edit.html',
         'edit': True},
		name='product'),

    url(r'^getnewcatalogproductpropertiesformblock$', 'getNewCatalogProductPropertiesFormBlock'),


)

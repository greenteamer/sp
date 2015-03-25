# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.conf.urls import patterns, url

urlpatterns = patterns('project.core.views',

    url(r'^viewproduct/$', 'viewProduct',
		{'template_name': 'core/viewproduct.html'},
		name='viewproduct'),

    # страница категорий
    url(r'^categories/$', 'categories',
		{'template_name': 'core/core_categories.html'},
		name='categories'),


    # страница одной категории
    url(r'^category-(?P<category_slug>[-\w]+)/$', 'coreCategory',
		{'template_name': 'core/core_category.html'},
		name='category'),

    # Главная страница
    url(r'^$', 'index_view',
		{'template_name': 'core/index.html'},
		name='catalog_home'),
    url(r'^purchase-(\d+)/$', 'corePurchase',
		{'template_name': 'core/core_purchase.html'},
		name='corePurchase'),
    url(r'^purchase-(?P<purchase_id>\d+)/catalog-(?P<catalog_id>\d+)/$', 'coreCatalog',
		{'template_name': 'core/core_catalog.html'},
		name='coreCatalog'),
     url(r'^purchase-(?P<purchase_id>\d+)/catalog-(?P<catalog_id>\d+)/product-(?P<product_id>\d+)/$', 'coreProduct',
		{'template_name': 'core/coreProduct.html'},
		name='coreProduct'),



    # Страницы сайта
    # url(r'^(?P<slug>[-\w]+)/$', 'page_view',
    #     {'template_name':'main/page.html'},
    #     name='page_view'),
)

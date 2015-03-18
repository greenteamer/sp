# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.conf.urls import patterns, url

urlpatterns = patterns('project.pristroy.views',

    # Главная страница раздела Пристрой
    url(r'^/$', 'Index',
		{'template_name': 'pristroy/index.html'},
		name='pristroy_catalog_home'),
    # добавить товар в пристрой
    url(r'^/add/$', 'CreateEditProduct',
		{'template_name': 'pristroy/pristroy_add_edit.html'},
		name='pristroy_add_edit'),
    # просмотр товара
    url(r'^/product-(?P<product_id>[-\d]+)$', 'ProductView',
		{'template_name': 'pristroy/product_view.html'},
		name='pristroy_product_view'),
    # редактировать товар
    url(r'^/product-(?P<product_id>[-\d]+)-edit$', 'CreateEditProduct',
		{'template_name': 'pristroy/pristroy_add_edit.html'},
		name='pristroy_add_edit'),
        # категория
    url(r'^/(?P<category_slug>[-\w]+)/$', 'Index',
		{'template_name': 'pristroy/index.html'},
		name='pristroy_category'),

)


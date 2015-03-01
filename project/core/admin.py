# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.contrib import admin
from project.core.models import *

class PropertiesInline(admin.StackedInline):
    model = Properties
    extra = 1

class ProductImagesInline(admin.StackedInline):
    model = ProductImages
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    model = Product
    # fieldsets = [
    #     (u'Основная информация', {'fields':['name','slug','body']}),
    #     (u'Специальная информация', {'fields': ['special_image','special_body']}),
    # ]
    inlines = [PropertiesInline, ProductImagesInline]
    # prepopulated_fields = {'slug':('name',)}

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImages)
admin.site.register(Properties)
admin.site.register(Catalog)
admin.site.register(CatalogProductProperties)
admin.site.register(Category)
admin.site.register(Purchase)

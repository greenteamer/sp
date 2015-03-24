# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.contrib import admin
from project.pristroy.models import *


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'category_slug': ('category_name',)}

class ProductImagesInline(admin.StackedInline):
    model = ProductImages
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImages)
admin.site.register(Category, CategoryAdmin)













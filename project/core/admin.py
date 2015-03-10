# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.contrib import admin
from project.core.models import *
from mptt_tree_editor.admin import TreeEditor

class CategoryAdmin(TreeEditor):
    """
    Управление категориями
    Как будут отображаться поля категорий в разделе администрирования
    """
    list_display = ("indented_short_title", "actions_column", 'name', 'created_at', 'updated_at',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['created_at']
    search_fields = ['name', 'description', 'meta_keywords', 'meta_description']
    readonly_fields = ('created_at', 'updated_at',)
    # exclude = ('created_at', 'updated_at',)
    prepopulated_fields = {'slug': ('name',)}


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
admin.site.register(Category, CategoryAdmin)
admin.site.register(Purchase)

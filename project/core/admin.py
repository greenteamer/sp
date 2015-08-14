# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.contrib import admin
from project.core.models import *
from mptt_tree_editor.admin import TreeEditor
from image_cropping import ImageCroppingMixin
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from ckeditor.widgets import CKEditorWidget


class PurchaseAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget()},
    }


class CategoryAdmin(TreeEditor):
    """
    Управление категориями
    Как будут отображаться поля категорий в разделе администрирования
    """
    list_display = (
        "indented_short_title", "actions_column", 'name',
        'created_at', 'updated_at',)

    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['created_at']
    search_fields = ['name', 'description', 'meta_keywords', 'meta_description']
    readonly_fields = ('created_at', 'updated_at',)
    # exclude = ('created_at', 'updated_at',)
    prepopulated_fields = {'slug': ('name',)}


class PurchaseStatusAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'status_name', 'status_description', 'status_icon',
        'status_priority']

    list_filter = ['status_name', 'status_priority']

# class PropertiesInline(admin.StackedInline):
#     model = Properties
#     extra = 1


class ProductImagesInline(ImageCroppingMixin, admin.StackedInline):
    model = ProductImages
    extra = 1


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product


class ProductAdmin(ImportExportActionModelAdmin):
    resource_class = ProductResource
    # model = Product
    # fieldsets = [
    #     (u'Основная информация', {'fields':['name','slug','body']}),
        # (u'Специальная информация', {
        #     'fields': ['special_image','special_body']}),
    # ]
    inlines = [ProductImagesInline]  # PropertiesInline
    # prepopulated_fields = {'slug':('name',)}


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImages)
# admin.site.register(Properties)
admin.site.register(Catalog)
admin.site.register(CatalogProductProperties)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Purchase)
admin.site.register(PurchaseStatus, PurchaseStatusAdmin)
admin.site.register(PurchaseStatusLinks)
admin.site.register(Slide)
admin.site.register(Promo)

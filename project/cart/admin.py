# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.contrib import admin
from project.cart.models import CartItem
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportMixin, ImportExportActionModelAdmin

class CartItemResource(resources.ModelResource):
    class Meta:
        model = CartItem

class CartItemAdmin(ImportExportActionModelAdmin):
    resource_class = CartItemResource
    pass

admin.site.register(CartItem, CartItemAdmin)

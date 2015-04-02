# -*- coding: utf-8 -*-
#!/usr/bin/env python
import decimal
import random
from models import CartItem
from project.core.models import Product, Purchase, Catalog
from django.shortcuts import get_object_or_404
from project.accounts.models import getProfile

def get_purchases_items(request):
    profile = getProfile(request.user)
    dict = {}
    list_items = []
    for purchase in Purchase.objects.filter(organizerProfile=profile):
        for catalog in Catalog.objects.filter(catalog_purchase=purchase):
            for product in Product.objects.filter(catalog=catalog):
                try:
                    items = CartItem.objects.filter(product=product)
                    if items:
                        list_items.extend(items)
                        # for item in items:
                        #     total = total+item.quantity*item.product.price
                except:
                    pass

            dict.update({catalog.catalog_name:list_items})

    return dict

# def get_purchases_items(request):
#     profile = getProfile(request.user)
#     dict = {}
#     list_items = []
#     for item in CartItem.objects.filter(user=request.user):
#         list_items.append(item)
#     # for catalog in Catalog.objects.all():
#     #     sorted_list = list_items.
#     # for purchase in Purchase.objects.filter(organizerProfile=profile):
#     #     for catalog in Catalog.objects.filter(catalog_purchase=purchase):
#     #         for product in Product.objects.filter(catalog=catalog):
#     #             try:
#     #                 items = CartItem.objects.filter(product=product)
#     #                 if items:
#     #                     list_items.extend(items)
#     #                     # for item in items:
#     #                     #     total = total+item.quantity*item.product.price
#     #             except:
#     #                 pass
#     #
#     dict.update({'catalog':list_items})
#
#     return dict

    # cart_items = CartItem.objects.filter(user=request.user)
    # cart_items.full_count = 0
    # for item in cart_items:
    #     cart_items.full_count = cart_items.full_count + item.quantity
    # return cart_items
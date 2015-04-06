# -*- coding: utf-8 -*-
#!/usr/bin/env python
from project.core.models import Product, Purchase, Catalog
from project.accounts.models import getProfile
from project.cart.models import CartItem


def get_purchases_dict(request):
    # посроение словаря для полного вывода данных о своих закупках для организатора
    # purchases_dict - словарь словарей
    # purchases_dict.keys() - Объекты закупок товары которых были добавлены в корзину участниками (купленных товаров)
    # purchases_dict.values() - словари вида {Каталог: [список объектов купленных товароов(cart_items)]}
    profile = getProfile(request.user)
    purchases_dict = {}
    for purchase in Purchase.objects.filter(organizerProfile=profile):
        purchase_dict = {}
        for catalog in Catalog.objects.filter(catalog_purchase=purchase):
            list_items = []
            for product in Product.objects.filter(catalog=catalog):
                try:
                    items = CartItem.objects.filter(product=product)
                    if items:
                        list_items.extend(items)
                except:
                    pass
            if list_items:
                purchase_dict.update({catalog: list_items})
        purchases_dict.update({purchase: purchase_dict})
    return purchases_dict


def get_all_purchases_dict(request):
    profile = getProfile(request.user)
    purchases_dict = {}
    for purchase in Purchase.objects.filter(organizerProfile=profile):
        purchase_dict = {}
        for catalog in Catalog.objects.filter(catalog_purchase=purchase):
            purchase_dict.update({catalog: Product.objects.filter(catalog=catalog)})
        purchases_dict.update({purchase: purchase_dict})
    return purchases_dict


def change_status(request):
    return True
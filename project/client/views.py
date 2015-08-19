# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from project.accounts.models import getProfile, OrganizerProfile, MemberProfile
from project.core.models import Purchase, Product, Promo, Catalog, Category
from project.cart.models import CartItem
from project.cart.forms import CartItemForm
from project.cart import cart
from project.helpers import check_profile
from project.cart.cart import add_to_cart
from project.accounts.forms import propertyForm, clientPropertyForm
import json

# rest
from rest_framework import serializers, viewsets, generics
from rest_framework.permissions import IsAuthenticated
from serializers import PurchaseSerializer, OrganizerSerializer, PromoSerializer, CategorySerializer


# Просмотр каталога
@check_profile
def clientAddToCartView(request):
    data = json.dumps({})
    if 'ajax' in request.POST:
        ajax = request.POST['ajax']

        if ajax == 'add_to_cart':
            # Добавление в корзину по аяксу
            product = Product.objects.get(id=request.POST['product'])
            list_properties = product.property.split(';')
            for item in list_properties:
                if request.POST['product_properties'] == item:
                    add_to_cart(request)    # Добавление в корзину
                    data = json.dumps({
                        'name': product.product_name
                    })

    return HttpResponse(data, content_type="application/json")



@check_profile
def indexView(request, template_name="client/pages/index.html"):
    big_content_purchase = Purchase.objects.get(id=2)  # TODO: сделать вывод нормальной закупки
    main_content_purchase = big_content_purchase  # TODO: сделать вывод нормальной закупки
    # создание формы свойств товара
    main_content_purchase.catalogs = main_content_purchase.get_catalogs()
    for catalog in main_content_purchase.catalogs.all():
        catalog.products = catalog.get_products()
        for product in catalog.products.all():
            product.form = clientPropertyForm(catalog.id)

    purchases = Purchase.objects.all()
    for purchase in purchases:
        purchase.products = set()
        catalogs = purchase.get_catalogs()
        for catalog in catalogs:
            purchase.products.update(catalog.get_products())
        purchase.products = list(purchase.products)[:3]

    if request.method == 'POST':
        """Добавляем товар в корзину
        используем стндартную форму для добавления товара
        котору мы дополучаем раньше для каждого товара"""
        product = Product.objects.get(id=request.POST['product'])
        product_properties = product.property   # все возможные свойства Этого товара
        if request.POST['product_properties'] in product_properties and request.POST['product_properties'] != '':
            # если выбранные св-ва есть в товаре
            cart_item = CartItem(product=product)
            form = CartItemForm(request.POST or None, instance=cart_item)
            if form.is_valid():
                cart_item = add_to_cart(request)    # Добавление в корзину

    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))


def clientCategoryView(request, category_slug, template_name="client/pages/category.html"):

    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))


@check_profile
def catalogView(request, template_name="client/pages/catalog.html"):
    purchases = Purchase.objects.all()
    for purchase in purchases:
        purchase.products = set()
        catalogs = purchase.get_catalogs()
        for catalog in catalogs:
            purchase.products.update(catalog.get_products())
        purchase.products = list(purchase.products)[:3]

    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))


def getAllPurchases(request):

    purchases_list = []
    purchases = Purchase.objects.all()
    for purchase in purchases:
        purchases_list.append({
            'name': purchase.name,
            'description': purchase.description
        })
    purchases = json.dumps(purchases_list)

    return HttpResponse(purchases, content_type="application/json")


# rest_framework


class PurchasesViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer


class OrganizersViewSet(viewsets.ModelViewSet):
    queryset = OrganizerProfile.objects.all()
    serializer_class = OrganizerSerializer


class PopularPromoViewSet(viewsets.ModelViewSet):
    queryset = Promo.objects.filter(alias='popular-promo')
    serializer_class = PromoSerializer


class NewPromoViewSet(viewsets.ModelViewSet):
    queryset = Promo.objects.filter(alias='new-promo')
    serializer_class = PromoSerializer


class HotPurchasesViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        purchases = []
        for purchase in Purchase.objects.all():
            if purchase.get_current_status().id == 5:
                purchases.append(purchase)

        return purchases


class CategoriwsViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


def getCartItems(request):
    items = []
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        items.append({
            'name': item.product.product_name,
            'image': "/media/%s" % item.product.get_image().image,
            'properties': item.properties,
            'price': item.product.price,
            'quantity': item.quantity
        })
    data = json.dumps(items)
    return HttpResponse(data, content_type="application/json")

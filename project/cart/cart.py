# -*- coding: utf-8 -*-
#!/usr/bin/env python
import decimal
import random
from models import CartItem
from project.core.models import Product
from django.shortcuts import get_object_or_404
from project.accounts.models import getProfile
from django.http.response import Http404, HttpResponseRedirect


CART_ID_SESSION_KEY = 'cart_id'

def _cart_id(request):
    """
      Получение id корзины из cookies для пользователя,
      или установка новых cookies если не существуют
      _модификатор для видимости в пределах модуля
      """
    if request.session.get(CART_ID_SESSION_KEY, '') == '':
        request.session[CART_ID_SESSION_KEY] = _generate_cart_id()
    return request.session[CART_ID_SESSION_KEY]

def _generate_cart_id():
    """Генерация уникального id корзины который будет хранится в cookies"""
    cart_id = ''
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
    cart_id_length = 50
    for y in range(cart_id_length):
        cart_id += characters[random.randint(0, len(characters) - 1)]
    return cart_id


def get_cart_items(request):
    cart_items = CartItem.objects.filter(user=request.user)
    cart_items.full_count = 0  # считаем колличество товаров для отображения в верхнем меню
    for item in cart_items:
        cart_items.full_count = cart_items.full_count + item.quantity
    return cart_items


# def getCartItemsForOrganizer(organizer):
#
#     return cart_items


def add_to_cart(request):
    """Добавление товара в корзину"""
    profile = getProfile(request.user)
    if profile.is_checked():
        postdata = request.POST.copy()
        product_id = postdata.get('product', '')
        quantity = postdata.get('quantity', 1)
        properties = postdata.get('product_properties', '')
        # Получаем товар, или возвращаем ошибку "не найден" если его не существует
        p = get_object_or_404(Product, id=product_id)
        # Получаем товары в корзине
        cart_products = get_cart_items(request)
        # Проверяем что продукт уже в корзине
        product_in_cart = False
        for cart_item in cart_products:
            # if (cart_item.product.id == p.id):    # Обновляем количество если найден
            if (cart_item.product.id == p.id and cart_item.properties == properties):  # Обновляем количество если найден товар с таким же ствойство
                cart_item.augment_quantity(quantity)
                product_in_cart = True
                return {'id': cart_item.id, 'quantity': quantity, 'properties': properties} # Возвратим данные записи в корзине

        if not product_in_cart:
            # Создаем и сохраняем новую корзину
            ci = CartItem()
            ci.product = p
            ci.quantity = quantity
            ci.cart_id = _cart_id(request)
            ci.user = request.user
            ci.properties = properties
            ci.save()
            return {'id': ci.id, 'quantity': quantity, 'properties': properties}  # Возвратим данные новой записи в корзине

def get_single_item(request, item_id):
    """Получаем конкретный товар в корзине"""
    return get_object_or_404(CartItem, id=item_id, user=request.user)


def remove_from_cart(request):
    """Удаляет выбранный товар из корзины"""
    postdata = request.POST.copy()
    item_id = postdata['item_id']
    cart_item = get_single_item(request, item_id)
    if cart_item:
        cart_item.delete()


def update_cart(request):
    """Обновляет количество отдельного товара"""
    postdata = request.POST.copy()
    item_id = postdata['item_id']
    quantity = postdata['quantity']
    cart_item = get_single_item(request, item_id)
    if cart_item:
        if quantity.isdigit() and int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()

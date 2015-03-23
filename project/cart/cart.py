# -*- coding: utf-8 -*-
#!/usr/bin/env python
import decimal
import random
from models import CartItem
from project.core.models import Product
from django.shortcuts import get_object_or_404

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
    """Получение всех товаров для текущей корзины"""
    return CartItem.objects.filter(cart_id=_cart_id(request))

def add_to_cart(request):
    """Добавление товара в корзину"""
    postdata = request.POST.copy()
    product_id = postdata.get('product', '')
    quantity = postdata.get('quantity', 1)
    # Получаем товар, или возвращаем ошибку "не найден" если его не существует
    p = get_object_or_404(Product, id=product_id)
    # Получаем товары в корзине
    cart_products = get_cart_items(request)
    # Проверяем что продукт уже в корзине
    product_in_cart = False
    for cart_item in cart_products:
        if (cart_item.product.id == p.id):
            # Обновляем количество если найден
            cart_item.augment_quantity(quantity)
            product_in_cart = True

    if not product_in_cart:
        # Создаем и сохраняем новую корзину
        ci = CartItem()
        ci.product = p
        ci.quantity = quantity
        ci.cart_id = _cart_id(request)
        ci.save()
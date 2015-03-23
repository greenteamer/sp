# -*- coding: utf-8 -*-
#!/usr/bin/env python
import decimal
import random

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
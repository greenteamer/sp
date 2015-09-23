# -*- coding: utf-8 -*-
#!/usr/bin/env python
import random
import copy
from underscore import _
from models import CartItem, Order
from project.core.models import Product, Purchase
from project.accounts.models import getProfile, OrganizerProfile
from project.settings import ADMIN_EMAIL
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string


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
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234\
        567890!@#$%^&*()'

    cart_id_length = 50
    for y in range(cart_id_length):
        cart_id += characters[random.randint(0, len(characters) - 1)]
    return cart_id


def get_cart_items(request):
    cart_items = CartItem.objects.filter(user=request.user)

    """считаем колличество товаров для отображения в верхнем меню"""
    cart_items.full_count = 0
    for item in cart_items:
        cart_items.full_count = cart_items.full_count + item.quantity
    return cart_items


def add_to_cart(request):
    """Добавление товара в корзину"""
    profile = getProfile(request.user)
    if profile.is_checked():
        postdata = request.POST.copy()
        product_id = postdata.get('product', '')
        quantity = postdata.get('quantity', 1)
        properties = postdata.get('product_properties', '')

        """Получаем товар, или возвращаем ошибку "не найден" если
        его не существует"""
        p = get_object_or_404(Product, id=product_id)


        """Получаем товары в корзине"""
        cart_products = get_cart_items(request)

        """Проверяем что продукт уже в корзине"""
        product_in_cart = False
        for cart_item in cart_products:
            """Обновляем количество если найден товар с таким же ствойством"""
            if (cart_item.product.id == p.id and cart_item.properties == properties):
                cart_item.augment_quantity(quantity)
                product_in_cart = True

                """Возвратим данные записи в корзине"""
                return {
                    'id': cart_item.id, 'quantity': quantity,
                    'properties': properties}

        if not product_in_cart:
            """Создаем и сохраняем новую корзину"""
            ci = CartItem()
            ci.product = p
            ci.quantity = quantity
            ci.cart_id = _cart_id(request)
            ci.user = request.user
            ci.properties = properties
            ci.save()
            """Возвратим данные новой записи в корзине"""
            return {'id': ci.id, 'quantity': quantity, 'properties': properties}


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


class HelperClass():
    """HelperClass
    создан что-бы нести в себе вспомогательные данные не отражающиеся в
    базе данных"""
    pass


def cart_stat(cart_items):
    """cart_stat
    Возвращает объект HelperClass, который несет в себе статистику по текущей
    карзине.
    в эту статистику на данный момент входят:
    items_count - общее количество добавленных в корзину товаров со всех закупок
    cart_total - общая стоимость корзины"""
    cart_stat = HelperClass()
    cart_stat.items_count = 0
    cart_stat.cart_total = 0.00

    for item in cart_items:
        cart_stat.cart_total += item.total_price()
        cart_stat.items_count += item.quantity

    return cart_stat


def create_data_for_export_cart_items(cart_items):
    """create_data_for_export_cart_items
    функция, которая принимает список cart_items одного каталога
    проверяет на совпадения купленных товаров разными пользоавтелями
    конкатенирует quantity CartItem и удаляет из списк повторяющиеся
    эллементы
    data - список списков, где 1 объект - список с заголовками колонок для xls
    """
    data = [[
        u'Артикул', u'Название товара', u'Свойство товара', u'Колличество']]

    tmp_data_copy = copy.deepcopy(cart_items)
    """глубокое копирование объектов внутри списка
    необходимо что-бы удалять CartItem из временного списка и формировать из
    него конечные данные data"""

    for tmp_item in tmp_data_copy:
        for item in cart_items:
            if tmp_item == item:
                pass

            elif tmp_item.product.sku == item.product.sku and tmp_item.properties == item.properties:
                tmp_item.quantity += item.quantity
                tmp_data_copy.remove(item)
                print tmp_data_copy
            else:
                pass

        data.append([
            tmp_item.product.sku, tmp_item.product.product_name,
            tmp_item.properties, tmp_item.quantity])
        """добавляем в data новый объект-список для xls"""

    return data


def getOrders(request):
    order_dict = {}
    total = 0
    # try:
    orders = Order.objects.filter(user=request.user)
    for order in orders:
        items = CartItem.objects.filter(order=order)                
        order.total = 0
        for item in items:
            order.total += item.quantity*item.product.price
        order_dict.update({order: items})
    # except:
    #     pass
    return order_dict


def send_messages(request ,dict):
    """ отправка сообщений организатору о том что человек заказл товары """

    purchase = Purchase.objects.get(id=request.POST['purchase_id'])    
    user_profile = getProfile(request.user)

    """список cartitems"""

    cart_items = []
    catalogs = dict[purchase]    
    for key, value in catalogs.items():
        for item in value:                    
            cart_items.append(item)
    
    is_no_ordered = _.some(cart_items, lambda x, *a: x.is_ordered == False)
    filtered_items = _.filter(cart_items, lambda x, *a: x.is_ordered == False)
    if is_no_ordered:
        # отправка организатору письма и заказчику
        # только при условии что есть незаказанные товары

        # создаем новый заказ и сохраняем в базу что бы обновить в дальнейшем наши cart итемы
        order = Order()
        order.user = request.user
        order.cart_id = filtered_items[0].cart_id
        order.purchase = purchase
        order.save()
        for item in filtered_items:
            item.is_ordered = True    
            item.order = order
            item.save()           

        context_dict = {
            'cart_items': cart_items,
            'name':  u"{}".format(purchase.organizerProfile.firstName)
        }
        subject = u'buybox.ru пользователь заказал товары'
        message = render_to_string('cart/organizer_email.html', context_dict)
        from_email = 'teamer777@gmail.com'
        to = purchase.organizerProfile.email
        msg = EmailMultiAlternatives(subject, message, from_email, [to])
        msg.content_subtype = "html"
        msg.send()

        # отправка письма участнику
        context_dict = {
            'cart_items': cart_items,
            'name':  u"{}".format(user_profile.firstName)
        }
        subject = u'buybox.ru Ваш заказа оформлен'
        message = render_to_string('cart/member_email.html', context_dict)
        from_email = 'teamer777@gmail.com'
        to = user_profile.email
        msg = EmailMultiAlternatives(subject, message, from_email, [to])
        msg.content_subtype = "html"
        msg.send()



















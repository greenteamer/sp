# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.template import RequestContext
from django.shortcuts import render_to_response
from project.cart.cart import get_cart_items, remove_from_cart,\
    update_cart

from project.cart import cart
from project.cart.forms import ExportForm
from project.cart.purchases import get_purchases_dict,\
    get_purchases_dict_for_user

from project.core.views import check_profile
from project.accounts.models import getProfile
from excel_response import ExcelResponse


@check_profile
def cartView(request, template_name):
    if request.method == 'POST':
        if 'remove' in request.POST:
            remove_from_cart(request)

        if 'update' in request.POST:
            update_cart(request)

    cart_items = get_cart_items(request)

    # возвращает Helper класс который содержит статистику по корзине
    cart_stat = cart.cart_stat(cart_items)

    # возвращает очень замущеный словарь
    dict = get_purchases_dict_for_user(request)

    return render_to_response(
        template_name, locals(), context_instance=RequestContext(request))


@check_profile
# TODO: настроить экспорт по закупкам
def purchasesCartView(request, template_name):
    # получаем словарь словарей ... описание в purchases.py
    purchases_dict = get_purchases_dict(request)
    form = ExportForm(request.POST or None)
    data = []
    if form.is_valid():
        postdata = request.POST.copy()
        if 'export' in postdata:
            # получаем каталог из словаря purchases_dict
            for dict_tmp in purchases_dict.values():
                for catalog, cart_items in dict_tmp.items():
                    if catalog.id == int(postdata['catalog']):
                        # data = [[
                        #     u'Название товара', u'Свойство товара',
                        #     u'Колличество', u'Фамилия', u'Имя', u'Телефон',
                        #     u'e-mail', u'Адрес', u'Дата бронирования']]

                        data = cart.create_data_for_export_cart_items(cart_items)
                        """передаем список cart_items каталога и получаем
                        сформированный список data для экпорта товаров в xls"""

            return ExcelResponse(data, 'catalog')

    return render_to_response(
        template_name, locals(), context_instance=RequestContext(request))

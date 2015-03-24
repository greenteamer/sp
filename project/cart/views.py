# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response, redirect
from project.cart.cart import add_to_cart, get_cart_items, remove_from_cart, update_cart
from project.cart.admin import CartItemResource, CartItem
from project.cart.purchases import get_purchases_items
from project.core.views import check_profile
from import_export import resources
from excel_response import ExcelResponse

@check_profile
def cartView(request, template_name):
    cart_items = get_cart_items(request)
    if request.method == 'POST':
        postdata = request.POST.copy()
        if postdata.has_key('remove'):
            remove_from_cart(request)
        if postdata.has_key('update'):
            update_cart(request)
        # if postdata.has_key('checkout'):
        #     checkout_url = checkout.get_checkout_url(request)
        #     return HttpResponseRedirect(checkout_url)
    return render_to_response(template_name, locals(),
                            context_instance=RequestContext(request))


@check_profile
def purchasesCartView(request, template_name):  # TODO: настроить экспорт по закупкам
    items = get_purchases_items(request)
    dict = get_purchases_items(request)
    # dataset = CartItemResource().export()
    # f = dataset.xls
    # f.to_encoding = 'utf-8'
    if  request.POST:
        postdata = request.POST.copy()
        if postdata.has_key('export'):
            items = CartItem.objects.all()
            return ExcelResponse(items)
    return render_to_response(template_name, locals(),
                            context_instance=RequestContext(request))
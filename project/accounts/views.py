# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.shortcuts import render
from project.accounts.profiles import retrieve
from project.accounts.models import OrganizerProfile, getOrganizerProfile
from project.accounts.forms import OrganizerProfileForm, purchaseForm
from project.core.forms import productForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from project.core.models import Purchase, Catalog, Product, CatalogProductProperties

from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404


def profileView(request, template_name):
    user = request.user
    form = OrganizerProfileForm()
    if user.is_authenticated():
        profile = getOrganizerProfile(user)
    else:
        return HttpResponseRedirect(urlresolvers.reverse('registrationView'))
    if request.method == "POST":
        form = OrganizerProfileForm(request.POST)
        if form.is_valid():
            form.save(request.user)

    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))

def registrationView(request, template_name):
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))


# __ Закупки __

# Просмотр всех закупок
def purchases(request, template_name):
    purchases = Purchase.objects.all()
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))

# Добавление закупки
def purchaseAdd(request, template_name):

    user = request.user

    """ проверяем пользователя и его профайл организатора"""
    if user.is_authenticated():
        profile = getOrganizerProfile(user)
    else:
        return HttpResponseRedirect(urlresolvers.reverse('registrationView'))

    message = ''
    if request.POST:
        form = purchaseForm(request.POST)
        if form.is_valid():
            form.save(user)
            message = u"Новая закупка «%s» успешно добавлена" % request.POST['name']
        else:
            message = u"Ошибка при добавлении закупки"

    purchase_form = purchaseForm()

    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))


# Просмотр или редактирование одной конкретной закупки (по id)
def purchase(request, purchase_id, template_name, edit=False):
    user = request.user

    """ проверяем пользователя и его профайл организатора"""
    if user.is_authenticated():
        profile = getOrganizerProfile(user)
    else:
        return HttpResponseRedirect(urlresolvers.reverse('registrationView'))

    message = ''
    if edit == True:  # если передан парамерт edit равный True, то редактируем закупку
        try:
            purchase = Purchase.objects.get(id=purchase_id)  # получаем экземпляр Закупки по id
            if request.POST:
                form = purchaseForm(request.POST)
                if form.is_valid():
                    purchase.name = request.POST['name']
                    purchase.save()
                    message = u"Закупка «%s» успешно изменена" % request.POST['name']
                else:
                    message = u"Ошибка при изменении закупки"

            purchase_form = purchaseForm(instance=purchase) # заполненная форма текущей закупки
            return render_to_response(template_name, locals(),
                                  context_instance=RequestContext(request))
        except ObjectDoesNotExist:
            raise Http404

    else:
        try:
            purchase = Purchase.objects.get(id=purchase_id)  # получаем экземпляр Закупки по id
        except ObjectDoesNotExist:
            raise Http404

        return render_to_response(template_name, locals(),
                                  context_instance=RequestContext(request))


# __ // Закупки __

# __ Каталоги __

# Просмотр всех каталогов для текущей закупки
def catalogs(request, purchase_id, template_name):
    try:
        purchase = Purchase.objects.get(id=purchase_id)
        catalogs = Catalog.objects.filter(purchase=purchase_id)
        # catalogs = Catalog.objects.all()
        return render_to_response(template_name, locals(),
                                  context_instance=RequestContext(request))
    except ObjectDoesNotExist:
            raise Http404

# Просмотр каталога
def catalog(request, purchase_id, catalog_id, template_name):
    try:
        purchase = Purchase.objects.get(id=purchase_id)
        catalog = Catalog.objects.get(id=catalog_id)
        catalog_product_properties = CatalogProductProperties.objects.filter(catalog=catalog_id)
        # catalogs = Catalog.objects.all()
        return render_to_response(template_name, locals(),
                                  context_instance=RequestContext(request))
    except ObjectDoesNotExist:
            raise Http404

# __ // Каталоги __


# __ Товары __

# Просмотр всех товаров для текущего каталога
def products(request, purchase_id, catalog_id, template_name):
    try:
        purchase = Purchase.objects.get(id=purchase_id)
        catalog = Catalog.objects.get(id=catalog_id)
        products = Product.objects.filter(catalog=catalog_id)
        return render_to_response(template_name, locals(),
                                  context_instance=RequestContext(request))
    except ObjectDoesNotExist:
            raise Http404

# Просмотр товара
def product(request, purchase_id, catalog_id, product_id, template_name):
    try:
        purchase = Purchase.objects.get(id=purchase_id)
        catalog = Catalog.objects.get(id=catalog_id)
        product = Product.objects.get(id=product_id)
        return render_to_response(template_name, locals(),
                                  context_instance=RequestContext(request))
    except ObjectDoesNotExist:
            raise Http404


# Добавление товара
def productAdd(request, catalog_id, template_name):
    try:
        message = ''
        user = request.user

        """ проверяем пользователя и его профайл организатора"""
        if user.is_authenticated():
            profile = getOrganizerProfile(user)
        else:
            return HttpResponseRedirect(urlresolvers.reverse('registrationView'))

        if request.POST:
            form = productForm(request.POST)
            if form.is_valid():
                form.save()
                message = u"Новый товар %s успешно добавлен" % request.POST['product_name']
            else:
                message = u"Ошибка при добавлении товара"

        product_form = productForm
        return render_to_response(template_name, locals(),
                                  context_instance=RequestContext(request))
    except ObjectDoesNotExist:
            raise Http404


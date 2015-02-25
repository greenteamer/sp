# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.http.response import HttpResponse
from django.shortcuts import render
from project.accounts.profiles import retrieve
from project.accounts.models import OrganizerProfile, getOrganizerProfile
from project.accounts.forms import OrganizerProfileForm, purchaseForm, catalogForm, catalogProductPropertiesForm
from project.core.forms import productForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from project.core.models import Purchase, Catalog, Product, CatalogProductProperties, Properties

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
        catalogs = Catalog.objects.filter(catalog_purchase=purchase_id)
        # catalogs = Catalog.objects.all()
        return render_to_response(template_name, locals(),
                                  context_instance=RequestContext(request))
    except ObjectDoesNotExist:
            raise Http404


        # # Добавление каталога
        # def catalogAdd(request, purchase_id, template_name):
        #
        #     user = request.user
        #
        #     """ проверяем пользователя и его профайл организатора"""
        #     if user.is_authenticated():
        #         profile = getOrganizerProfile(user)
        #     else:
        #         return HttpResponseRedirect(urlresolvers.reverse('registrationView'))
        #
        #     message = ''
        #     if request.POST:
        #         form = catalogForm(request.POST)
        #         if form.is_valid():
        #             form.save(purchase_id)  # каталог сохраняется для нужной закупки - переопределена ф-я save
        #             message = u"Новый каталог «%s» успешно добавлен. <br/> Добавить еще: " % request.POST['name']
        #         else:
        #             message = u"Ошибка при добавлении каталога"
        #
        #     purchase_form = catalogForm()
        #
        #     return render_to_response(template_name, locals(),
        #                               context_instance=RequestContext(request))

# Добавление каталога
def catalogAdd(request, purchase_id, template_name):

    user = request.user

    """ проверяем пользователя и его профайл организатора"""
    if user.is_authenticated():
        profile = getOrganizerProfile(user)
    else:
        return HttpResponseRedirect(urlresolvers.reverse('registrationView'))

    message = ''
    if request.POST:
        catalog_form = catalogForm(request.POST)
        catalogProductProperties_form = catalogProductPropertiesForm(request.POST)
        if catalog_form.is_valid() and catalogProductProperties_form.is_valid():
            new_catalogProductProperties = catalogProductProperties_form.save(commit=False)
            new_catalogProductProperties.cpp_catalog = catalog_form.save(purchase_id)  # каталог сохраняется для нужной закупки - переопределена ф-я save, возвращает созданный объект каталога
            new_catalogProductProperties.cpp_purchase = Purchase.objects.get(id=purchase_id)
            new_catalogProductProperties.save()
            message = u"Новый каталог «%s» успешно добавлен. <br/> Добавить еще: " % request.POST['catalog_name']
        else:
            message = u"Ошибка при добавлении каталога"

    catalog_form = catalogForm()
    catalogProductProperties_form = catalogProductPropertiesForm()

    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))


# Просмотр каталога
def catalog(request, purchase_id, catalog_id, template_name):
    try:
        purchase = Purchase.objects.get(id=purchase_id)
        catalog = Catalog.objects.get(id=catalog_id)
        catalog_product_properties = CatalogProductProperties.objects.filter(cpp_catalog=catalog_id)
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

        catalog_product_properties = CatalogProductProperties.objects.filter(cpp_catalog=catalog_id)

        # all_properties = {1: "one", 2: "two", 3: "three"}
        all_properties = {}
        i = 0
        for catalog_product_propertie in catalog_product_properties:
            i += 1
            properties = Properties.objects.filter(properties_product=product_id)
            for propertie in properties:
                all_properties.update({catalog_product_propertie.cpp_name: propertie.properties_name})

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


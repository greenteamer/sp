# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.shortcuts import render
from django.template import RequestContext
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.core.context_processors import csrf
from project.core.models import Purchase, Product, Catalog, CatalogProductProperties
from project.core.functions import *
from project.accounts.models import getOrganizerProfile
from project.accounts.forms import OrganizerProfileForm, UserRegistrationForm, purchaseForm, catalogForm, catalogProductPropertiesForm, ProductForm, propertyForm
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404

def index_view(request, template_name="catalog/index.html"):
    user = request.user
    purchases = Purchase.objects.all()
    # if user.is_authenticated():
    #     """проверка есть ли профиль у пользователя и получение его файл accounts.models"""
    #     profile = getOrganizerProfile(user)
    # else:
    #     return HttpResponseRedirect(urlresolvers.reverse('registrationView'))
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))



def viewProduct(request, template_name="core/viewproduct.html"):
    products = Product.objects.all()
    if template_name == 0:
        return products
    else:
        return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))


# Просмотр или редактирование одной конкретной закупки (по id)
def corePurchase(request, purchase_id, template_name):
    user = request.user

    message = ''

    try:
        purchase = Purchase.objects.get(id=purchase_id)  # получаем экземпляр Закупки по id
        catalogs = Catalog.objects.filter(catalog_purchase=purchase)
    except ObjectDoesNotExist:
        raise Http404

    return render_to_response(template_name, locals(),
                                  context_instance=RequestContext(request))


# Просмотр каталога
def coreCatalog(request, purchase_id, catalog_id, template_name):
    try:
        purchase = Purchase.objects.get(id=purchase_id)
        catalog = Catalog.objects.get(id=catalog_id)

        # catalog_product_properties = CatalogProductProperties.objects.filter(cpp_catalog=catalog_id)
        # catalogs = Catalog.objects.all()
        return render_to_response(template_name, locals(),
                                  context_instance=RequestContext(request))
    except ObjectDoesNotExist:
            raise Http404
# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.shortcuts import render
from django.template import RequestContext
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.core.context_processors import csrf
from project.core.models import Purchase, Product, Catalog, ProductImages, Category
from project.accounts.models import getProfile, OrganizerProfile, MemberProfile
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404

def index_view(request, template_name="catalog/index.html"):
    user = request.user
    """ проверяем пользователя и его профайл организатора"""
    if user.is_authenticated():
         profile = getProfile(user)
         if profile is None: return HttpResponseRedirect(urlresolvers.reverse('populateProfileView'))
         elif not profile.is_checked(): return HttpResponseRedirect(urlresolvers.reverse('profileView'))
    else:
        return HttpResponseRedirect(urlresolvers.reverse('registrationView'))
    # groups = user.groups.all()
    # try:
    #     user.groups.get(name='member')
    # except Exception:
    #     note = u'Пожалуйста зарегистрируйтесь как участник закупок'

    purchases = Purchase.objects.all()
    # if user.is_authenticated():
    #     """проверка есть ли профиль у пользователя и получение его файл accounts.models"""
    #     profile = getOrganizerProfile(user)
    # else:
    #     return HttpResponseRedirect(urlresolvers.reverse('registrationView'))
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))


#  страница для тестов
def viewProduct(request, template_name="core/viewproduct.html"):
    # products = Product.objects.all()

    # products = Product.objects.raw('SELECT * FROM core_product')
    """ проверяем пользователя и его профайл организатора"""
    user = request.user
    if user.is_authenticated():
         profile = getProfile(user)
         if profile is None: return HttpResponseRedirect(urlresolvers.reverse('populateProfileView'))
         elif not profile.is_checked(): return HttpResponseRedirect(urlresolvers.reverse('profileView'))
    else:
        return HttpResponseRedirect(urlresolvers.reverse('registrationView'))
    # пример прямого sql запроса для выборки из двух таблиц за один раз
    products = Product.objects.raw('select core_product.id, core_product.product_name, core_productimages.image '
                                   'from core_product, core_productimages '
                                   'where core_product.id = core_productimages.p_image_product_id')

    product_images = ProductImages.objects.all()
    product = Product.objects.order_by('-id')[0]

    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))



def categories(request, template_name):
    """ проверяем пользователя и его профайл организатора"""
    user = request.user
    if user.is_authenticated():
         profile = getProfile(user)
         if profile is None: return HttpResponseRedirect(urlresolvers.reverse('populateProfileView'))
         elif not profile.is_checked(): return HttpResponseRedirect(urlresolvers.reverse('profileView'))
    else:
        return HttpResponseRedirect(urlresolvers.reverse('registrationView'))

    return render_to_response(template_name, locals(),
                            context_instance=RequestContext(request))


# Страница категории
def coreCategory(request, category_slug, template_name):

    """ проверяем пользователя и его профайл организатора"""
    user = request.user
    if user.is_authenticated():
         profile = getProfile(user)
         if profile is None: return HttpResponseRedirect(urlresolvers.reverse('populateProfileView'))
         elif not profile.is_checked(): return HttpResponseRedirect(urlresolvers.reverse('profileView'))
    else:
        return HttpResponseRedirect(urlresolvers.reverse('registrationView'))

    try:
        category_id = Category.objects.get(slug=category_slug)
    except ObjectDoesNotExist:
            raise Http404

    purchases = Purchase.objects.filter(categories=category_id)

    return render_to_response(template_name, locals(),
                            context_instance=RequestContext(request))





# Просмотр или редактирование одной конкретной закупки (по id)
def corePurchase(request, purchase_id, template_name):
    """ проверяем пользователя и его профайл организатора"""
    user = request.user
    if user.is_authenticated():
         profile = getProfile(user)
         if profile is None: return HttpResponseRedirect(urlresolvers.reverse('populateProfileView'))
         elif not profile.is_checked(): return HttpResponseRedirect(urlresolvers.reverse('profileView'))
    else:
        return HttpResponseRedirect(urlresolvers.reverse('registrationView'))

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
    """ проверяем пользователя и его профайл организатора"""
    user = request.user
    if user.is_authenticated():
         profile = getProfile(user)
         if profile is None: return HttpResponseRedirect(urlresolvers.reverse('populateProfileView'))
         elif not profile.is_checked(): return HttpResponseRedirect(urlresolvers.reverse('profileView'))
    else:
        return HttpResponseRedirect(urlresolvers.reverse('registrationView'))

    try:
        purchase = Purchase.objects.get(id=purchase_id)
        catalog = Catalog.objects.get(id=catalog_id)

        # catalog_product_properties = CatalogProductProperties.objects.filter(cpp_catalog=catalog_id)
        # catalogs = Catalog.objects.all()
        return render_to_response(template_name, locals(),
                                  context_instance=RequestContext(request))
    except ObjectDoesNotExist:
            raise Http404


def checkOrganizerProfile(user):
    try:
        profile = OrganizerProfile.objects.get(user=user)
        if profile.is_checked():
            return profile
    except:
        return None
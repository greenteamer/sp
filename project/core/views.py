# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.shortcuts import render
from django.template import RequestContext
from django.core import urlresolvers
from django.http import HttpResponseRedirect
import datetime
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.core.context_processors import csrf
from project.cart.models import CartItem
from project.cart.forms import CartItemForm
from project.cart.cart import add_to_cart, get_cart_items
from project.core.models import Purchase, Product, Catalog, ProductImages, Category
from project.accounts.models import getProfile, OrganizerProfile, MemberProfile
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse, Http404
from django.contrib import messages
# from project.accounts.forms import propertyForm


"""декоратор проверки профиля пользователя
принимает пользователя , возвращяет профайл"""
def check_profile(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            profile = getProfile(request.user)
            if profile is None:
                messages.info(request, "Пожалуйста заполните Ваш профиль")
                return redirect('/profile/populate-profile/')
            elif not profile.is_checked():
                messages.info(request, "Ваш профиль еще не проверен")
                return redirect('/profile/')
            else:
                return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/profile/registration/')
    return wrapper


@check_profile
def index_view(request, template_name="catalog/index.html"):
    purchases = Purchase.objects.all()
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))


#  страница для тестов
@check_profile
def viewProduct(request, template_name="core/viewproduct.html"):
    # пример прямого sql запроса для выборки из двух таблиц за один раз
    products = Product.objects.raw('select core_product.id, core_product.product_name, core_productimages.image '
                                   'from core_product, core_productimages '
                                   'where core_product.id = core_productimages.p_image_product_id')
    product_images = ProductImages.objects.all()
    product = Product.objects.order_by('-id')[0]
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))


@check_profile
def categories(request, template_name):
    return render_to_response(template_name, locals(),
                            context_instance=RequestContext(request))


# Страница категории
@check_profile
def coreCategory(request, category_slug, template_name):
    try:
        category_id = Category.objects.get(slug=category_slug)
    except ObjectDoesNotExist:
            raise Http404
    purchases = Purchase.objects.filter(categories=category_id)
    return render_to_response(template_name, locals(),
                            context_instance=RequestContext(request))


# Просмотр или редактирование одной конкретной закупки (по id)
@check_profile
def corePurchase(request, purchase_id, template_name):
    """ проверяем пользователя и его профайл организатора"""
    user = request.user
    if user.is_authenticated():
         profile = getProfile(user)
         if profile is None: return HttpResponseRedirect(urlresolvers.reverse('populateProfileView'))
         elif not profile.is_checked(): return HttpResponseRedirect(urlresolvers.reverse('profileView'))
    else:
        return HttpResponseRedirect(urlresolvers.reverse('registrationView'))
    # message = ''
    try:
        purchase = Purchase.objects.get(id=purchase_id)  # получаем экземпляр Закупки по id
        catalogs = Catalog.objects.filter(catalog_purchase=purchase)
    except ObjectDoesNotExist:
        raise Http404

    return render_to_response(template_name, locals(),
                                  context_instance=RequestContext(request))


# Просмотр каталога
@check_profile
def coreCatalog(request, purchase_id, catalog_id, template_name):  # TODO: реализовать ajax добавление в корзину
    try:
        purchase = Purchase.objects.get(id=purchase_id)
        catalog = Catalog.objects.get(id=catalog_id)

        # catalog_product_properties = CatalogProductProperties.objects.filter(cpp_catalog=catalog_id)
        # catalogs = Catalog.objects.all()
        return render_to_response(template_name, locals(),
                                  context_instance=RequestContext(request))
    except ObjectDoesNotExist:
            raise Http404


# Просмотр товара
@check_profile
def coreProduct(request, purchase_id, catalog_id, product_id, template_name):  # TODO: реализовать ajax добавление в корзину
    try:

        try:
            ajax = request.POST['ajax']
        except:
            ajax = False

        # Добавление в корзину по аяксу
        if ajax != False:
            product = Product.objects.get(id=request.POST['product'])
            product_properties = product.property   # все возможные свойства Этого товара
            if request.POST['product_properties'] in product_properties and request.POST['product_properties'] != '':
                # если выбранные св-ва есть в товаре
                cart_item = CartItem(product=product)
                form = CartItemForm(request.POST or None, instance=cart_item)
                if form.is_valid():
                    cart_item = add_to_cart(request)    # Добавление в корзину
                    ajax_return = '{"status":"ok", "cart_item_id":"%d", "quantity":"%s", "properties":"%s"}' % (cart_item['id'], cart_item['quantity'], cart_item['properties'])
                else:
                    ajax_return = '{"status":"error"}'
                return HttpResponse(ajax_return)
            else:
                return HttpResponse('{"status":"no"}')

        product = Product.objects.get(id=product_id)
        # property_form = propertyForm(catalog_id)
        images = ProductImages.objects.filter(p_image_product=product_id)
        cart_item = CartItem(product=product)
        form = CartItemForm(request.POST or None, instance=cart_item)
        if form.is_valid():
            add_to_cart(request)
        return render_to_response(template_name, locals(),
                                  context_instance=RequestContext(request))
    except ObjectDoesNotExist:
            raise Http404









# страница для обработки ajax запросов
def ajaxquery(request):

    # TODO: удалить эту вьюху нафиг
    product = Product.objects.get(id=request.GET['product_id'])
    product_properties = product.property
    if request.GET['product_properties'] in product_properties and request.GET['product_properties'] != '':
        return HttpResponse('ok')
    else:
        return HttpResponse('no')

    # return HttpResponse(product_properties)





# def checkOrganizerProfile(user):
#     try:
#         profile = OrganizerProfile.objects.get(user=user)
#         if profile.is_checked():
#             return profile
#     except:
#         return None
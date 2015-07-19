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
from project.core.models import Purchase, Product, Catalog, ProductImages, Category, PurchaseQuestion, PurchaseAnswer, CatalogProductProperties
from project.accounts.models import getProfile, OrganizerProfile, MemberProfile
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse, Http404
from django.contrib import messages
from project.accounts.forms import propertyForm

def check_profile(func):
    """декоратор проверки профиля пользователя
    принимает пользователя , возвращяет профайл"""
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
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


@check_profile
def categories(request, template_name):
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

# Страница категории
@check_profile
def coreCategory(request, category_slug, template_name):
    try:
        category_id = Category.objects.get(slug=category_slug)
        all_categories = Category.objects.filter(parent=category_id)
        if len(all_categories) > 0:
            purchases = set()
            for category in all_categories:
                purchases_set = set(Purchase.objects.filter(categories=category))
                purchases = purchases | purchases_set
        else:
            purchases = Purchase.objects.filter(categories=category_id)
    except ObjectDoesNotExist:
        raise Http404
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


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

        if 'question' in request.POST:
            new_question = PurchaseQuestion()
            new_question.purchase_id = purchase_id
            new_question.text = request.POST['question']
            new_question.user = user
            new_question.save()

        if 'answer' in request.POST:
            new_answer = PurchaseAnswer()
            new_answer.question_id = request.POST['question_id']
            new_answer.text = request.POST['answer']
            new_answer.user = user
            new_answer.save()

    except ObjectDoesNotExist:
        raise Http404

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


# Просмотр каталога
@check_profile
def coreCatalog(request, purchase_id, catalog_id, template_name):
    try:

        if 'ajax' in request.POST:
            ajax = request.POST['ajax']

            if ajax == 'get_product_images':
                product = Product.objects.get(id=request.POST['product'])
                images = product.get_all_image()

                result = ''
                for image in images:
                    result = result + '<img style="width:200px;height:auto; float:left;" src="' + image.url() + '">'

                return HttpResponse(result)



            if ajax == 'add_to_cart':
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
                            image = product.get_image()
                            ajax_return = '{"status":"ok", "cart_item_id":"%d", "quantity":"%s", "properties":"%s", "product_name":"%s", "product_image":"%s", "product_url":"%s"}' % \
                                          (cart_item['id'], cart_item['quantity'], cart_item['properties'], product.product_name, image.url(), product.url_core())
                        else:
                            ajax_return = '{"status":"error"}'
                        return HttpResponse(ajax_return)
                    else:
                        return HttpResponse('{"status":"no"}')
            else:
                return HttpResponse('no_ajax')

        purchase = Purchase.objects.get(id=purchase_id)

        if 'product_property' in request.GET:

            property = request.GET['product_property']
            # property = "34"
            products = Product.objects.filter(property__icontains=property)
            current_request = ""
            for key, value in request.GET.items():
                if key != 'product_property':
                    current_request += u"%s %s " % (key, value)
        else:
            products = Catalog.objects.get(id=catalog_id).get_products()

        catalog_properties = CatalogProductProperties.objects.filter(cpp_catalog_id=catalog_id)
        # purchase = Purchase.objects.get(id=purchase_id)
        catalog = Catalog.objects.get(id=catalog_id)
        # id = catalog_id
        property_form = propertyForm(catalog_id)

        return render_to_response(
            template_name, locals(), context_instance=RequestContext(request))

    except ObjectDoesNotExist:
            raise Http404


# Просмотр товара
@check_profile
def coreProduct(request, purchase_id, catalog_id, product_id, template_name):
    try:
        if 'ajax' in request.POST:
            ajax = request.POST['ajax']
            # Добавление в корзину по аяксу
            if ajax is not False:
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
        property_form = propertyForm(catalog_id)
        # images = ProductImages.objects.filter(p_image_product=product_id)
        images = product.get_all_image()


        cart_item = CartItem(product=product)
        cart_form = CartItemForm(request.POST or None, instance=cart_item)
        if cart_form.is_valid():
            add_to_cart(request)

        if 'ajax' in request.GET:
            return render_to_response('core/core_product_ajax.html', locals(),
                                  context_instance=RequestContext(request))
        else:
            return render_to_response(template_name, locals(),
                                  context_instance=RequestContext(request))
    except ObjectDoesNotExist:
            raise Http404

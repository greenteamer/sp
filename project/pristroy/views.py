# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404, HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from forms import ProductForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from models import Product, Category

# страница пристроя, и страницы категорий пристроя
def Index(request, template_name, category_slug=False):

    if category_slug == False:
        products = Product.objects.all()
    else:
        try:
            category = Category.objects.get(category_slug=category_slug)
            products = Product.objects.filter(product_catalog=category.id)
        except ObjectDoesNotExist:
            raise Http404

    paginator = Paginator(products, 3)
    page = request.GET.get('page')

    try:
        page_products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_products = paginator.page(paginator.num_pages)


    # return HttpResponse()
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))


# Просмотр товара
def ProductView(request, template_name, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except ObjectDoesNotExist:
        raise Http404
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))


# создание товара в пристрой
def CreateEditProduct(request, template_name, product_id=False):

    if request.POST:
        if product_id == False:
            product_form = ProductForm(request.POST)
        else:
            product = Product.objects.get(id=product_id)
            product_form = ProductForm(request.POST, instance=product)
        if product_form.is_valid():
            product_save = product_form.save()
            # product.product_name = request.POST['product_name']
            # product.description = request.POST['description']
            # product.price = request.POST['price']
            # product.sku = request.POST['sku']
            # product.save()
            message = 'Сохранено'
        else:
            message = 'Поля заполенен не верно'

    if product_id == False:
        product_form = ProductForm
    else:
        product = Product.objects.get(id=product_id)
        product_form = ProductForm(instance=product)

    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))




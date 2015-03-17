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



def CreateProduct(request, template_name):

    product_form = ProductForm


    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))




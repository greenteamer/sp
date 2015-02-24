# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from forms import ProductForm, PropertiesForm, ProductFormCustom
from django.core.context_processors import csrf
from project.core.models import *
from project.core.functions import *

def index_view(request, template_name="catalog/index.html"):

    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))


def addProduct(request, template_name="core/addproduct.html"):
    message = ''
    if request.POST:
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            message = u"Новый товар %s успешно добавлен" % request.POST['name']

        # product = Product()
        # product.name = '111' #request.POST['name']
        # product.description = '11'
        # product.price = 11
        # product.sku = 11
        # product.catalog = Catalog.objects.get(pk=1)
        # product.save()

        else:
            message = u"Ошибка при добавлении товара"



    form2 = ProductFormCustom


    # else:
    product = Product.objects.get(pk=1)
    product_form = ProductForm#(instance=product)
    property_form = PropertiesForm
    args = {}
    args.update(csrf(request))
    # args['article'] = Article.objects.get(id=article_id)
    # args['comments'] = Comments.objects.filter(comments_article_id=article_id)
    args['message'] = message
    args['form2'] = form2
    args['product_form'] = product_form
    # args['property_form']= property_form
    # args['username'] = auth.get_user(request).username
    return render_to_response(template_name, args)


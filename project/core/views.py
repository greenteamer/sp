# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.shortcuts import render
from django.template import RequestContext
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from forms import productForm, propertiesForm#, productFormCustom
from django.core.context_processors import csrf
from project.core.models import *
from project.core.functions import *
from project.accounts.models import getOrganizerProfile

def index_view(request, template_name="catalog/index.html"):
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))



def viewProduct(request, template_name="core/viewproduct.html"):
    products = Product.objects.all()
    if template_name == 0:
        return products
    else:
        return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))


def addProduct(request, template_name="core/addproduct.html"):
    message = ''
    user = request.user

    """ проверяем пользователя и его профайл организатора"""
    if user.is_authenticated():
        profile = getOrganizerProfile(request, user)
    else:
        return HttpResponseRedirect(urlresolvers.reverse('registrationView'))

    if request.POST:
        form = productForm(request.POST)
        if form.is_valid():
            form.save()
            message = u"Новый товар %s успешно добавлен" % request.POST['product_name']
        else:
            message = u"Ошибка при добавлении товара"

    product_form = productForm#(instance=product)
    property_form = propertiesForm
    # args['article'] = Article.objects.get(id=article_id)
    # args['comments'] = Comments.objects.filter(comments_article_id=article_id)
    purchase = Purchase.objects.all()
    products = viewProduct(request, 0)
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))

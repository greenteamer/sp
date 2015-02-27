# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.shortcuts import render
from django.template import RequestContext
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
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



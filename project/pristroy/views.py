# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404, HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from django.http import HttpResponseRedirect




def Index(request, template_name):

    # return HttpResponse()
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))

# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.shortcuts import render
from project.accounts.profiles import retrieve
from project.accounts.models import OrganizerProfile, getOrganizerProfile
from project.accounts.forms import OrganizerProfileForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from django.http import HttpResponseRedirect

def profileView(request, template_name):
    user = request.user
    form = OrganizerProfileForm()
    if user.is_authenticated():
        profile = getOrganizerProfile(request, user)
    else:
        return HttpResponseRedirect(urlresolvers.reverse('registrationView'))
    if request.method == "POST":
        form = OrganizerProfileForm(request.POST)
        if form.is_valid():
            form.save(request.user)

    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))

def registrationView(request, template_name):
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))

# Create your views here.

# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.shortcuts import render
from project.accounts.profiles import retrieve
from project.accounts.models import OrganizerProfile, getOrganizerProfile
from project.accounts.forms import OrganizerProfileForm, UserRegistrationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from project.settings import ADMIN_EMAIL
from django.core.mail import send_mail, EmailMultiAlternatives

def profileView(request, template_name):
    user = request.user
    form = OrganizerProfileForm()
    if user.is_authenticated():
        profile = getOrganizerProfile(request, user)
    else:
        return HttpResponseRedirect(urlresolvers.reverse('registrationView'))
    if request.method == "POST":
        form = OrganizerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(request.user)

    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))

def registrationView(request, template_name):
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = UserRegistrationForm(postdata)
        if form.is_valid():
            form.save()
            un = postdata.get('username', '')
            # name="password1" т.к. два поля с подтверждением
            pw = postdata.get('password1', '')
            new_user = authenticate(username=un, password=pw)
            if new_user and new_user.is_active:

                # отправляем e-mail о регистрации нового пользователя
                subject = u'sp.ru регистрация %s' % new_user.username
                message = u' Зарегистрирован новый пользователь %s' % (new_user.username)
                send_mail(subject, message, 'teamer777@gmail.com', [ADMIN_EMAIL], fail_silently=False)

                login(request, new_user)
                # Редирект на url с именем my_account
                url = urlresolvers.reverse('profileView')
                return HttpResponseRedirect(url)
    else:
        form = UserRegistrationForm()
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))

# Create your views here.

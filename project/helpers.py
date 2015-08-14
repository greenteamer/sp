# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from project.accounts.models import getProfile
from django.contrib import messages


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

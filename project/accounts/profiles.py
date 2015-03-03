# -*- coding: utf-8 -*-
#!/usr/bin/env python
from project.accounts.models import OrganizerProfile
# from project.core.models import Purchase
# from webshop.accounts.forms import UserProfileForm


def retrieve(request):
    """Возвращает экземпляр класса форма профиля пользователя"""
    try:
        profile = request.user.get_profile()
    # если у пользователя не было профиля, то создаем его
    except OrganizerProfile.DoesNotExist:
        profile = OrganizerProfile(user=request.user)
        profile.save()
    return profile

def set(request):
    """Заполняем форму данными пользователя"""
    profile = retrieve(request)
    profile_form = OrganizerProfile(request.POST, instance=profile)
    profile_form.save()


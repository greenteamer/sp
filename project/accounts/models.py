# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.db import models
import random
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
# from project.core.models import Purchase
from django.core.exceptions import ObjectDoesNotExist


class BaseUserInfo(models.Model):
    """Абстрактный класс для заказов"""
    class Meta:
        abstract = True

    # Контактная информация
    email = models.EmailField(max_length=50, verbose_name=(u'Ваш email'))
    phone = models.CharField(max_length=20, verbose_name=(u'Ваш телефон'))
    firstName = models.CharField(max_length=50, verbose_name=(u'Имя'))
    lastName = models.CharField(max_length=50, verbose_name=(u'Фамилия'))
    address = models.CharField(max_length=50, verbose_name=(u'Адрес'))
    city = models.CharField(max_length=50, verbose_name=(u'Город'))
    zipCode = models.CharField(max_length=10, verbose_name=(u'Почтовый индекс'))


class OrganizerProfile(BaseUserInfo):
    """Профиль пользователя"""
    user = models.OneToOneField(User, unique=True)
    icon = models.FileField(
        u'Image', upload_to='accounts/images/', help_text=u'Фото', blank=True)

    organizer_checked = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = _(u'Профили организаторов')

    def is_checked(self):
        return self.organizer_checked is True

    def __unicode__(self):
        return _(u'Профиль: ') + self.user.username

    def get_full_name(self):
        return u"%s %s" % (self.firstName, self.lastName)

    def get_purchases(self):
        from project.core.models import Purchase
        return Purchase.objects.filter(organizerProfile=self)

    def getOrganizerPurchases(self):
        from project.core.models import Purchase
        try:
            profiles = Purchase.objects.filter(organizerProfile=self)
            for profile in profiles:
                #используется для вывода статуса закупки (демо режим)
                profile.bar = random.randrange(20, 90, 1)
            return profiles
        except:
            return None


class MemberProfile(BaseUserInfo):
    """Профиль пользователя"""
    user = models.OneToOneField(User, unique=True)
    icon = models.FileField(
        u'Image', upload_to='accounts/images/', help_text=u'Фото', blank=True)

    member_checked = models.BooleanField(default=False)

    def is_checked(self):
        return self.member_checked is True

    def get_full_name(self):
        return u"%s %s" % (self.firstName, self.lastName)

    def __unicode__(self):
        return _(u'Профиль: ') + self.user.username

    class Meta:
        verbose_name_plural = _(u'Профили участников')


def getProfile(user):
    try:
        try:
            return OrganizerProfile.objects.get(user=user)
        except:
            return MemberProfile.objects.get(user=user)
    except ObjectDoesNotExist:
        return None


def repopulateProfile(profile, request):
    profile.firstName = request.POST['firstName']
    profile.lastName = request.POST['lastName']
    profile.email = request.POST['email']
    profile.phone = request.POST['phone']
    profile.address = request.POST['address']
    profile.city = request.POST['city']
    profile.zipCode = request.POST['zipCode']
    if request.FILES:
        profile.icon = request.FILES['icon']
    return profile

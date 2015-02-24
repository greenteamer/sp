# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

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
    icon = models.FileField(_(u'Image'), upload_to='accounts/images/',
                             help_text=u'Фото', blank=True)

    def __unicode__(self):
        return _(u'Профиль: ') + self.user.username
    class Meta:
        verbose_name_plural = _(u'Профили организаторов')


"""проверка есть ли профиль у пользователя и получение его"""
def getOrganizerProfile(user):
    try:
        profile = OrganizerProfile.objects.get(user=user)
    except:
        profile = None
    return profile

def handle_uploaded_file(f):
    destination = open('some/file/name.txt', 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.db import models
from django.contrib.auth.models import User
from project.accounts.models import OrganizerProfile, MemberProfile
from project.core.models import Product, Catalog, Purchase
from project.cart.models import CartItem


class Notification(models.Model):
    name = models.CharField(verbose_name=u'Заголовок уведомления', max_length=240, unique=False)
    description = models.TextField(verbose_name=u'Текст уведомления')
    choice = models.CharField(verbose_name=u'Выбор назначения',
                              max_length=240,
                              choices=(
                                  ('purchase', u'Изменение закупки'),
                                  ('status', u'Изменение статуса'),
                                  ('organizer', u'Организаторам'),
                                  ('member', u'Участникам'),
                                  ('all', u'Всем')
                              ),
                              default='all')
    users_list = models.TextField(verbose_name=u'Список профайлов',
                                  help_text=u'Заполняется автоматически при сохранении', blank=True, null=True)

    def __unicode__(self):
        return self.name

    def organizer_choice(self):
        profiles = OrganizerProfile.objects.all()
        u_list = set()
        for profile in profiles:
            u_list.add(str(profile.user.id))
        self.users_list = u_list
        return u_list

    def member_choice(self):
        profiles = MemberProfile.objects.all()
        u_list = set()
        for profile in profiles:
            u_list.add(str(profile.user.id))
        self.users_list = u_list
        return u_list

    def purchase_choice(self, purchase):
        catalogs = Catalog.objects.filter(catalog_purchase=purchase.id)
        products = set()
        u_list = set()
        for catalog in catalogs:
            products = products | set(Product.objects.filter(catalog=catalog))
        for product in products:
            cart_items = CartItem.objects.filter(product=product)
            for item in cart_items:
                u_list.add(str(item.user.id))
        return ', '.join(u_list)

    def status_choice(self, status):
        purchase = Purchase.objects.get(id=status.purchase_id)
        catalogs = Catalog.objects.filter(catalog_purchase=purchase)
        products = set()
        u_list = set()
        for catalog in catalogs:
            products = products | set(Product.objects.filter(catalog=catalog))
        for product in products:
            cart_items = CartItem.objects.filter(product=product)
            for item in cart_items:
                u_list.add(str(item.user.id))
        return ', '.join(u_list)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.choice == 'organizer':
            self.users_list = ', '.join(self.organizer_choice())
        elif self.choice == 'member':
            self.users_list = ', '.join(self.member_choice())
        elif self.choice == 'all':
            self.users_list = self.organizer_choice() | self.member_choice()
            self.users_list = ', '.join(self.users_list)

        return super(Notification, self).save(force_insert, force_update, using)
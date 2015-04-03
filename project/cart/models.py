# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django.db import models
from project.core.models import Product
from project.accounts.models import OrganizerProfile, MemberProfile
from django.contrib.auth.models import User

class CartItem(models.Model):  # TODO: добавить profile_member и profile_organizer
    cart_id = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey(Product, unique=False)
    user = models.ForeignKey(User)
    properties = models.CharField(max_length=250, verbose_name=u'Свойства товара', default='')

    def name(self):
        return self.product.product_name
    def augment_quantity(self, quantity):
        """Изменение количества товара в корзине"""
        if quantity.isdigit():
            self.quantity = self.quantity + int(quantity)
            self.save()
    def total_price(self):
        return self.quantity*self.product.price
    def get_organizer(self):
        try:
            return OrganizerProfile.objects.get(user=self.user)
        except:
            None
    def get_member(self):
        try:
            return MemberProfile.objects.get(user=self.user)
        except:
            None
    def __unicode__(self):
        return self.product.product_name



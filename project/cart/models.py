# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django.db import models
from project.core.models import Product

class CartItem(models.Model):
    cart_id = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey(Product, unique=False)

    def name(self):
        return self.product.name
    def augment_quantity(self, quantity):
        """Изменение количества товара в корзине"""
        if quantity.isdigit():
            self.quantity = self.quantity + int(quantity)
            self.save()
# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.contrib import admin
from project.cart.models import CartItem


admin.site.register(CartItem)

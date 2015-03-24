# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django import forms
from models import CartItem

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        widgets = {'product': forms.HiddenInput(),}
        exclude = ('cart_id', 'user')
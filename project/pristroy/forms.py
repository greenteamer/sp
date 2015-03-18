# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm, Form
from models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
        # пример фукнции map
        # def f(field):
        #     self.fields[field].widget.attrs = {'class': 'form-control'}
        # map(f, self.fields)



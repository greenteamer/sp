# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm, Form
from models import Product, Properties


class ProductForm(ModelForm):
    class Meta:
        model = Product
        # fields = ['comments_text']

class PropertiesForm(ModelForm):
    class Meta:
        model = Properties
        # fields = ['name', 'catalogProductProperties']


class ProductFormCustom(forms.Form):
    field1 = forms.CharField()
    field2 = forms.IntegerField()
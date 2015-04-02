# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm, Form
from models import Product, ProductImages


class ProductForm(ModelForm):
    class Meta:
        model = Product
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'placeholder': self.fields[field].label, 'class': 'form-control'}
        # пример фукнции map
        # def f(field):
        #     self.fields[field].widget.attrs = {'class': 'form-control'}
        # map(f, self.fields)



class ProductImagesForm(ModelForm):
    class Meta:
        model = ProductImages
        exclude = ('p_image_product',)
    def __init__(self, *args, **kwargs):
        super(ProductImagesForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs = {'class': 'btn btn-block btn-default btn-sm', 'multiple': 'multiple'}  #
    def save(self, product_id):
        obj = super(ProductImagesForm, self).save(commit=False)
        obj.p_image_product = Product.objects.get(id=product_id)
        obj.save()
        return obj





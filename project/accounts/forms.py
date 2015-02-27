# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django import forms
from project.accounts.models import OrganizerProfile, getOrganizerProfile
from project.core.models import Purchase, Catalog, CatalogProductProperties, Product
from django.forms import ModelForm, Form
from project.core.functions import *


class OrganizerProfileForm(forms.ModelForm):
    class Meta:
        model = OrganizerProfile
        # widgets = {'user': forms.HiddenInput()}
        exclude = ('user',)

    def save(self, user):
        obj = super(OrganizerProfileForm, self).save(commit=False)
        obj.user = user
        return obj.save()


class purchaseForm(ModelForm):
    class Meta:
        model = Purchase
        exclude = ('organizerProfile',)

    def save(self, user):
        obj = super(purchaseForm, self).save(commit=False)
        obj.organizerProfile = getOrganizerProfile(user)
        obj.save()
        # assert isinstance(obj, object) #pycharm сам влепил
        return obj


class catalogForm(ModelForm):
    class Meta:
        model = Catalog
        exclude = ('catalog_purchase',)
    def save(self, purchase_id):
        # TODO: сделать валидацию на существование закупки (purchase_id)
        obj = super(catalogForm, self).save(commit=False)
        obj.catalog_purchase = Purchase.objects.get(id=purchase_id)
        obj.save()
        return obj


class catalogProductPropertiesForm(ModelForm):
    class Meta:
        model = CatalogProductProperties
        fields = ["cpp_name", "cpp_values"]


class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ('catalog',)
    def save(self, catalog_id):
        # TODO: сделать валидацию на существование каталога (catalog_id)
        obj = super(ProductForm, self).save(commit=False)
        obj.catalog = Catalog.objects.get(id=catalog_id)
        obj.save()
        return obj



def propertyForm(catalog_id):

    cpp_obj = CatalogProductProperties.objects.filter(cpp_catalog_id=catalog_id)
    list = []
    for cpp_object in cpp_obj:
        values = cpp_object.cpp_values.split(";")
        local_dict = {}
        for value in values:
            local_dict.update({value: cpp_object.cpp_name})
        list.append(local_dict)

    #return list
    class DynamicPropertyForm(forms.Form):

        def __init__(self, *args, **kwargs):
            super(DynamicPropertyForm, self).__init__(*args, **kwargs)

            for dict_item in list:
                list_choices = []
                for key, value in dict_item.items():
                    list_choices.append([key, key])
                    name = value
                slug = translit(name).lower()
                self.fields['%s' % slug] = forms.ChoiceField(widget=forms.RadioSelect, label=name, choices=list_choices)

    return DynamicPropertyForm()




# class testFrom(forms.Form):
    # flieds, sdfdf, sdfd  = [forms.CharField(),forms.CharField(),forms.CharField()]
    #
    # flied = forms.CharField()
    # sdfdf = forms.CharField()
    # sdfd = forms.CharField()
    #
    # choice_field = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)












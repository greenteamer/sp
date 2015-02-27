# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django import forms
from project.accounts.models import OrganizerProfile, getOrganizerProfile
from project.core.models import Purchase, Catalog, CatalogProductProperties, Product
from django.forms import ModelForm, Form

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


class productForm(ModelForm):
    class Meta:
        model = Product
        # fields = ['comments_text']


#///////////////////////////////////////////////////////////////////////////////////////////
def get_dinamic_form(catalog_id):
    cpp_obj = CatalogProductProperties.objects.filter(cpp_catalog_id=catalog_id)
    class testForm(forms.Form):
        # fields = CatalogProductProperties.all_field()
        # for cpp_object in cpp_obj:
        #     cpp_object.cpp_name = forms.CharField()
        field1 = forms.CharField()
        # field2 = forms.IntegerField()
    return testForm()


def get_user_form_for_user(user):
    class UserForm(forms.Form):
        username = forms.CharField()
        fields = user.get_profile().all_field()
        #Use field to find what to show.
#
# all_properties = {}
#         for property in properties:
#             current_catalog_product_properties = CatalogProductProperties.objects.get(id=property.properties_catalogProductProperties_id)
#             all_properties.update({current_catalog_product_properties.cpp_name: property.properties_name.split(";")})  # формируется словарь вида {имя_свойства: значения_распарсенные_в_список}

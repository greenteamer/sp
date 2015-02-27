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



# class productForm(forms.Form):
    # flieds, sdfdf, sdfd  = [forms.CharField(),forms.CharField(),forms.CharField()]
    #
    # flied = forms.CharField()
    # sdfdf = forms.CharField()
    # sdfd = forms.CharField()
    #
    # choice_field = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)


    #
    # def _init_(self, *args, **kwargs):
    #     super(productForm, self)._init_(args, kwargs)
    #
    #     # args should be a list with the single QueryDict (GET or POST dict)
    #     # that you passed it
    #     for k,v in args[0].items():
    #         if k.startswith('Q') and k not in self.fields.keys():
    #             self.fields[k] = TestCharField(initial=v, required=True)
    #
    #

#///////////////////////////////////////////////////////////////////////////////////////////
def get_dinamic_form(catalog_id):
    cpp_obj = CatalogProductProperties.objects.filter(cpp_catalog_id=catalog_id)

    list = []
    CHOISES = {}

    for cpp_object in cpp_obj:
        values = cpp_object.cpp_values.split(";")
        local_dict = {}
        for value in values:
            local_dict.update({value: value})
        list.append(local_dict)

    class ProductForm(forms.Form):
        # for list_item in list:
        #       choise = forms.CharField()
        a = [12, 34]
        b = [44, 66]
        c = [24, 34]
        CHOICES = [a, b, c]
        choice_field = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

    return ProductForm












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

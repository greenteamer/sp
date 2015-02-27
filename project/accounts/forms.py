# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _
from captcha.fields import CaptchaField
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

class UserRegistrationForm(forms.ModelForm):

    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    username = forms.RegexField(label=_("Username"), max_length=100,
        regex=r'^[\w.@+-]+$',
        help_text = u"Пожалуйста введите имя пользователя не более 40 символов",
        error_messages = {
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text = _("Enter the same password as above, for verification."))
    captcha = CaptchaField(label=u'Введите символы с картинки')

    class Meta:
        model = User
        fields = ("username",)

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_password(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



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














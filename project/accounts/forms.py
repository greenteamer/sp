# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from project.accounts.models import OrganizerProfile, getProfile, MemberProfile
from project.core.models import Purchase, Catalog, CatalogProductProperties,\
    Product, ProductImages

from django.forms import ModelForm
from project.core.functions import *
from ckeditor.widgets import CKEditorWidget


class OrganizerProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrganizerProfileForm, self).__init__(*args, **kwargs)
        self.fields['firstName'].widget.attrs = {
            'placeholder': 'Ваше Имя', 'class': 'form-control'}

        self.fields['lastName'].widget.attrs = {
            'placeholder': 'Ваша Фамилия', 'class': 'form-control'}

        self.fields['email'].widget.attrs = {
            'placeholder': 'Ваш e-mail', 'class': 'form-control'}

        self.fields['phone'].widget.attrs = {
            'placeholder': 'Ваш телефон', 'class': 'form-control'}

        self.fields['address'].widget.attrs = {
            'placeholder': 'Ваш адрес', 'class': 'form-control'}

        self.fields['city'].widget.attrs = {
            'placeholder': 'Ваш город', 'class': 'form-control'}

        self.fields['zipCode'].widget.attrs = {
            'placeholder': 'Почтовый индекс', 'class': 'form-control'}

        self.fields['icon'].widget.attrs = {
            'class': 'btn btn-block btn-default btn-sm'}

    class Meta:
        model = OrganizerProfile
        # widgets = {'user': forms.HiddenInput()}
        exclude = ('user',)

    def save(self, user):
        obj = super(OrganizerProfileForm, self).save(commit=False)
        obj.user = user
        return obj.save()


class MemberProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MemberProfileForm, self).__init__(*args, **kwargs)
        self.fields['firstName'].widget.attrs = {
            'placeholder': 'Ваше Имя', 'class': 'form-control'}

        self.fields['lastName'].widget.attrs = {
            'placeholder': 'Ваша Фамилия', 'class': 'form-control'}

        self.fields['email'].widget.attrs = {
            'placeholder': 'Ваш e-mail', 'class': 'form-control'}

        self.fields['phone'].widget.attrs = {
            'placeholder': 'Ваш телефон', 'class': 'form-control'}

        self.fields['address'].widget.attrs = {
            'placeholder': 'Ваш адрес', 'class': 'form-control'}

        self.fields['city'].widget.attrs = {
            'placeholder': 'Ваш город', 'class': 'form-control'}

        self.fields['zipCode'].widget.attrs = {
            'placeholder': 'Почтовый индекс', 'class': 'form-control'}

        self.fields['icon'].widget.attrs = {
            'class': 'btn btn-block btn-default btn-sm'}

    class Meta:
        model = MemberProfile
        exclude = ('user',)

    def save(self, user):
        obj = super(MemberProfileForm, self).save(commit=False)
        obj.user = user
        return obj.save()


class UserRegistrationForm(forms.ModelForm):
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    username = forms.RegexField(
        label=_("Username"),
        max_length=100,
        regex=r'^[\w.@+-]+$',
        error_messages={
            'invalid': "Это значение может состоять из латинских букв,\
            цифр и знаков @/./+/-/_."},

        widget=forms.TextInput(attrs={
            'placeholder': 'Ваш логин на анг.',
            'class': 'form-control floating-label',
            'id': 'focusedInput'
            # 'data-hint': 'Например: supersaler'
        }),
    )
    email = forms.EmailField(
        label=_("Email"),
        error_messages={
            'invalid': "Введите корректный e-mail адрес"},

        widget=forms.TextInput(attrs={
            'placeholder': 'Ваш e-mail',
            'class': 'form-control floating-label'
        }),
    )

    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Введите пароль',
            'class': 'form-control',
            'class': 'form-control floating-label',
        })
    )

    class Meta:
        model = User
        fields = ("username",)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.ModelForm):
    error_messages = {
        'wrong': ("Имя пользователя или пароль введены неверно"),
    }
    username = forms.RegexField(
        label=_("Username"),
        max_length=100,
        regex=r'^[\w.@+-]+$',
        error_messages={
            'invalid': "Это значение может состоять из латинских букв,\
            цифр и знаков @/./+/-/_."},
        widget=forms.TextInput(attrs={
            'placeholder': 'Ваше Имя', 'class': 'form-control'
        }),
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Введите пароль', 'class': 'form-control'
        })
    )

    class Meta:
        model = User
        fields = ("username",)


class purchaseForm(ModelForm):
    class Meta:
        model = Purchase
        exclude = ('organizerProfile',)

    def __init__(self, *args, **kwargs):
        super(purchaseForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {
                'placeholder': self.fields[field].label,
                'class': 'form-control'
            }
        self.fields['description'].widget = CKEditorWidget(
            config_name='interface')
        # self.fields['description'].widget.attrs = {
        #     'placeholder': self.fields['description'].label,
        #     'rows': '10', 'class': 'form-control'
        # }

    def save(self, user):
        obj = super(purchaseForm, self).save(commit=False)
        obj.organizerProfile = getProfile(user)
        obj.save()
        return obj


class catalogForm(ModelForm):
    class Meta:
        model = Catalog
        exclude = ('catalog_purchase',)

    def __init__(self, *args, **kwargs):
        super(catalogForm, self).__init__(*args, **kwargs)
        self.fields['catalog_name'].widget.attrs = {
            'placeholder': 'Введите название каталога',
            'class': 'form-control'
        }

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

    def __init__(self, *args, **kwargs):
        super(catalogProductPropertiesForm, self).__init__(*args, **kwargs)
        self.fields['cpp_name'].widget.attrs = {
            'placeholder': 'Введите свойство для товаров в этом каталоге',
            'class': 'form-control'
        }
        self.fields['cpp_values'].widget.attrs = {
            'placeholder': 'Введите возможные значения для свойства\
             через символ ";"',
            'class': 'form-control'
        }


class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ('catalog', 'property')

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['product_name'].widget.attrs = {'class': 'form-control'}
        self.fields['description'].widget.attrs = {'class': 'form-control'}
        self.fields['price'].widget.attrs = {'class': 'form-control'}
        self.fields['sku'].widget.attrs = {'class': 'form-control'}

    def save(self, catalog_id, sv=''):
        # TODO: сделать валидацию на существование каталога (catalog_id)
        obj = super(ProductForm, self).save(commit=False)
        obj.catalog = Catalog.objects.get(id=catalog_id)
        obj.property = sv
        obj.save()
        return obj


class ProductImagesForm(ModelForm):
    class Meta:
        model = ProductImages
        exclude = ('p_image_product', 'cropping')

    def __init__(self, *args, **kwargs):
        super(ProductImagesForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs = {
            'class': 'btn btn-block btn-default btn-sm'
        }
        self.fields['p_image_title'].widget.attrs = {'class': 'form-control'}

    def save(self, product_id):
        obj = super(ProductImagesForm, self).save(commit=False)
        obj.p_image_product = Product.objects.get(id=product_id)
        obj.save()
        return obj


# TODO: желательно сделать выбор по умолчанию каждого из свойств.\
#на данный момент реализованно через jquery
def propertyForm(catalog_id, product_id=False):
    """динамичная форма свойств.перечисляет свойства выбранного каталога"""
    cpp_obj = CatalogProductProperties.objects.filter(cpp_catalog_id=catalog_id)
    list = []
    for cpp_object in cpp_obj:
        values = cpp_object.cpp_values.split(";")
        local_dict = {}
        for value in values:
            local_dict.update({value: cpp_object.cpp_name})
        list.append(local_dict)

    # return list
    class DynamicPropertyForm(forms.Form):

        def __init__(self, *args, **kwargs):
            super(DynamicPropertyForm, self).__init__(*args, **kwargs)

            for dict_item in list:
                list_choices = []
                for key, value in dict_item.items():
                    list_choices.append([key, key])
                    name = value
                slug = translit(name).lower()

                # if product_id is not False:
                #     cpp_id = CatalogProductProperties.objects.get(
                #         cpp_slug=slug)
                #     try:
                #         property_value = Properties.objects.get(
                #             properties_catalogProductProperties_id=cpp_id,
                #             properties_product_id=product_id
                #         )
                #         self.fields[slug] = forms.ChoiceField(
                #             widget=forms.RadioSelect,
                #             label=name,
                #             choices=list_choices,
                #             initial=property_value.properties_value
                #         )
                #     except:
                #         self.fields[slug] = forms.ChoiceField(
                #             widget=forms.RadioSelect,
                #             label=name,
                #             choices=list_choices
                #         )
                # else:
                self.fields[slug] = forms.ChoiceField(
                    widget=forms.RadioSelect,
                    label=name, choices=list_choices)

    return DynamicPropertyForm()

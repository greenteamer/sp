# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django import forms
from django.contrib.auth.models import User
from models import CartItem

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        widgets = {'product': forms.HiddenInput(),}
        exclude = ('cart_id',)

# class OrganizerProfileForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(OrganizerProfileForm, self).__init__(*args, **kwargs)
#         self.fields['firstName'].widget.attrs = {'placeholder':'Ваше Имя', 'class':'form-control'}
#         self.fields['lastName'].widget.attrs = {'placeholder':'Ваша Фамилия', 'class':'form-control'}
#         self.fields['email'].widget.attrs = {'placeholder':'Ваш e-mail', 'class':'form-control'}
#         self.fields['phone'].widget.attrs = {'placeholder':'Ваш телефон', 'class':'form-control'}
#         self.fields['address'].widget.attrs = {'placeholder':'Ваш адрес', 'class':'form-control'}
#         self.fields['city'].widget.attrs = {'placeholder':'Ваш город', 'class':'form-control'}
#         self.fields['zipCode'].widget.attrs = {'placeholder':'Почтовый индекс', 'class':'form-control'}
#         self.fields['icon'].widget.attrs = {'class':'btn btn-block btn-default btn-sm'}
#     class Meta:
#         model = OrganizerProfile
#         # widgets = {'user': forms.HiddenInput()}
#         exclude = ('user',)
#     def save(self, user):
#         obj = super(OrganizerProfileForm, self).save(commit=False)
#         obj.user = user
#         return obj.save()
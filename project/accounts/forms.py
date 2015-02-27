# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django import forms
from django.contrib.auth.models import User
from django.contrib import auth
from django.utils.translation import ugettext, ugettext_lazy as _
from captcha.fields import CaptchaField
from project.accounts.models import OrganizerProfile, getOrganizerProfile
from project.core.models import Purchase
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

class UserRegistrationForm(forms.ModelForm):
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    username = forms.RegexField(label=_("Username"), max_length=100,
        regex=r'^[\w.@+-]+$',
        error_messages = {'invalid': "Это значение может состоять из латинских букв, цифр и знаков @/./+/-/_."},
        widget=forms.TextInput(attrs={'placeholder': 'Ваше Имя', 'class': 'form-control'}),
    )
    email = forms.EmailField(
        label=_("Email"),
        error_messages = {'invalid': "Введите корректный e-mail адрес"},
        widget=forms.TextInput(attrs={'placeholder': 'Ваш e-mail', 'class': 'form-control'}),
    )
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль', 'class': 'form-control'})
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
    username = forms.RegexField(label=_("Username"), max_length=100,
        regex=r'^[\w.@+-]+$',
        error_messages = {'invalid': "Это значение может состоять из латинских букв, цифр и знаков @/./+/-/_."},
        widget=forms.TextInput(attrs={'placeholder': 'Ваше Имя', 'class': 'form-control'}),
    )
    password = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль', 'class': 'form-control'})
    )
    class Meta:
        model = User
        fields = ("username",)

    # def clean_username(self):
    #     username = self.cleaned_data["username"]
    #     try:
    #         User.objects.get(username=username)
    #     except User.DoesNotExist:
    #         return username
    #     raise forms.ValidationError(self.error_messages['duplicate_username'])

    # def auth_user(self):
    #     username = self.cleaned_data["username"]
    #     password = self.cleaned_data["password"]
    #     try:
    #         User.objects.get(username=username)
    #         user = auth.authenticate(username=username, password=password)
    #         return user
    #     except User.DoesNotExist:
    #         return forms.ValidationError(self.error_messages['wrong'])

class purchaseForm(ModelForm):
    class Meta:
        model = Purchase
        exclude = ('organizerProfile',)

    def save(self, user):
        obj = super(purchaseForm, self).save(commit=False)
        obj.organizerProfile = getOrganizerProfile(user)
        return obj.save()


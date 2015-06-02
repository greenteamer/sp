# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm, Form
from models import ImportFiles


class ImportXLSForm(forms.ModelForm):
    class Meta:
        model = ImportFiles


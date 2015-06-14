# -*- coding: utf-8 -*-
from django import forms
from models import ImportFiles


class ImportXLSForm(forms.ModelForm):
    class Meta:
        model = ImportFiles

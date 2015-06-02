# -*- coding: utf-8 -*-
from django import forms
from crispy_forms.helper import FormHelper




def setup_bootstrap_helpers(object):
    object.helper = FormHelper()
    object.helper.form_class = 'angular_form'
    object.helper.field_class = 'form-control floating-label'

# -*- coding: utf-8 -*-
from django import forms
from djangular.forms import NgFormValidationMixin, NgModelFormMixin
from crispy_forms.helper import FormHelper
from project.notifications.models import Notification


class NoticeForm(NgModelFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NoticeForm, self).__init__(*args, **kwargs)
        setup_bootstrap_helpers(self)

    class Meta:
        model = Notification
        fields = ('name', 'description', 'choice')


def setup_bootstrap_helpers(object):
    object.helper = FormHelper()
    object.helper.form_class = 'angular_form'
    object.helper.field_class = 'form-control floating-label'

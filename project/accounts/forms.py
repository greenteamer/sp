# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django import forms
from project.accounts.models import OrganizerProfile

class OrganizerProfileForm(forms.ModelForm):
    class Meta:
        model = OrganizerProfile
        # widgets = {'user': forms.HiddenInput()}
        exclude = ('user',)

    def save(self, user):
        obj = super(OrganizerProfileForm, self).save(commit=False)
        obj.user = user
        return obj.save()
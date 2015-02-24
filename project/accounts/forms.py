# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django import forms
from project.accounts.models import OrganizerProfile

class OrganizerProfileForm(forms.ModelForm):
    class Meta:
        model = OrganizerProfile
        # exclude = ('user',)
# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django.contrib import admin
from django.contrib.auth.models import User
from project.accounts.models import BaseUserInfo, OrganizerProfile
# Register your models here.

# class UserInline(admin.StackedInline):
#     """Вывод заказов списком"""
#     model = User
#     extra = 0

# class UserProfileAdmin(admin.ModelAdmin):
#     model = UserProfile
#     inlines = [UserInline]

admin.site.register(OrganizerProfile)

